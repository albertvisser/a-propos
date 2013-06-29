# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import logging
from .apomixin import Apomixin, languages
HERE = os.path.split(__file__)[0]

class Page(gui.QFrame):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, mf):
        gui.QFrame.__init__(self)
        self.txt = gui.QTextEdit(self)
        ## self.txt.Bind(wx.EVT_KEY_DOWN, mf.on_key)
        ## # self.Bind(wx.EVT_TEXT, self.OnEvtText, self.txt)
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.txt)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

class CheckDialog(gui.QDialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option=""):
        self.parent = parent
        self.option = option
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.apoicon)
        txt = gui.QLabel(message)
        self.check = gui.QCheckBox("Deze melding niet meer laten zien", self)
        ok_button = gui.QPushButton("&Ok", self)
        self.connect(ok_button, core.SIGNAL('clicked()'), self.klaar)
        vbox = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.exec_()

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.opts[self.option] = False
        gui.QDialog.done(self, 0)

class MainFrame(gui.QMainWindow, Apomixin):
    """main class voor de applicatie

    subclass van Apomixin voor het gui-onafhankelijke gedeelte
    """
    def __init__(self, parent=None):
        gui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Apropos")
        self.move(10, 10)
        self.resize(650, 400)
        self.apoicon = gui.QIcon(os.path.join(HERE, "apropos.ico"))
        self.setWindowIcon(self.apoicon)
        self.tray_icon = gui.QSystemTrayIcon(self.apoicon, self)
        self.tray_icon.setToolTip("Click to revive Apropos")
        self.connect(self.tray_icon, core.SIGNAL('clicked'),
            self.revive)
        tray_signal = "activated(QSystemTrayIcon::ActivationReason)"
        self.connect(self.tray_icon, core.SIGNAL(tray_signal),
            self.revive)
        self.tray_icon.hide()

        self.nb = gui.QTabWidget(self)
        self.setCentralWidget(self.nb)
        self.nb.currentChanged.connect(self.page_changed)
        # pagina sluiten op dubbel - of middelklik
        ## self.nb.setTabsClosable(True) # workaround: sluitgadgets
        self.nb.tabCloseRequested.connect(self.closetab)

        self.initapp()

    def page_changed(self, event=None):         # werkt!
        """pagina aanpassen nadat een andere gekozen is
        """
        n = self.nb.count()
        self.current = self.nb.currentIndex()
        print("page_changed: current is", self.current)
        currentpage = self.nb.currentWidget() # self.nb.widget(self.current)
        print("page_changed: widget is", currentpage)
        currentpage.txt.setFocus()
        ## if True: # os.name == 'nt':
        ## if sys.platform == 'win32':
            ## event.Skip()

    def keyPressEvent(self, e):                 # werkt!
        skip = self.on_key(e)
        if not skip:
            gui.QMainWindow.keyPressEvent(self, e)

    def on_key(self, e):                        # werkt!
        """afhandeling toetsaanslagen / toetsencombinaties
        """
        skip = False
        keycode = e.key()
        keymods = e.modifiers()
        if keymods == core.Qt.ControlModifier:
            if keycode == core.Qt.Key_L:
                aant = self.nb.count()
                widgets = [self.nb.widget(x) for x in range(aant)]
                self.nb.clear()
                for wdg in widgets:
                    wdg.destroy()
                self.initapp()
                self.meld('(Re)loaded')
                skip = True
            elif keycode == core.Qt.Key_N:
                self.newtab()
                skip = True
            elif keycode == core.Qt.Key_W:
                self.closetab(self.current)
                skip = True
            # elif keycode == core.Qt.Key_LEFT:
                # self.nb.AdvanceSelection(False)
                # skip = True
            # elif keycode == core.Qt.Key_RIGHT:
                # self.nb.AdvanceSelection()
                # skip = True
            elif keycode == core.Qt.Key_H:
                if self.opts["AskBeforeHide"]:
                    dlg = CheckDialog(self, 'Apropos',
                        message=languages[self.opts["language"]]["hide_text"],
                        option='AskBeforeHide')
                self.tray_icon.show()
                self.hide()
                skip = True
            elif keycode == core.Qt.Key_S:
                self.afsl()
                if self.opts["NotifyOnSave"]:
                    dlg = CheckDialog(self, 'Apropos',
                        message=languages[self.opts["language"]]["save_text"],
                        option='NotifyOnSave')
                skip = True
            elif keycode == core.Qt.Key_Q:
                self.close()
                ## self.afsl()
                ## self.Destroy()
                skip = True
            elif keycode == core.Qt.Key_F1:
                self.choose_language()
                skip = True
        elif keycode == core.Qt.Key_F1:
            self.helppage()
            skip = True
        elif keycode == core.Qt.Key_F2:
            self.asktitle()
            skip = True
        elif keycode == core.Qt.Key_Escape:
            self.close()
            skip = True
        return skip

    ## def onLeftDblClick(self, event=None):
        ## """reageert op dubbelklikken op tab t.b.v. verwijderen pagina
        ## """
        ## self.x = event.GetX()
        ## self.y = event.GetY()
        ## item, flags = self.nb.HitTest((self.x, self.y))
        ## self.nb.DeletePage(item)
        ## event.Skip()

    def initapp(self):                          # werkt!
        """initialiseer de applicatie
        """
        self.opts = {"AskBeforeHide":True, "ActiveTab":0, 'language': 'eng',
            'NotifyOnSave': True}
        self.load_notes()
        if self.apodata:
            for i, x in self.apodata.items():
                if i == 0 and "AskBeforeHide" in x:
                    for key, val in x.items():
                        self.opts[key] = val
                else:
                    self.newtab(titel=x[0], note=x[1])
            self.current = self.opts["ActiveTab"]
            self.nb.setCurrentIndex(self.current)
        else:
            self.newtab()
            self.current = 0

    def newtab(self, titel=None, note=None):    # werkt!
        """initialiseer een nieuwe tab
        """
        nieuw = self.nb.count() + 1
        if titel is None:
            titel = str(nieuw)
        newpage = Page(mf=self)
        if note is not None:
            newpage.txt.setText(note)
        self.nb.addTab(newpage, titel)
        self.nb.setCurrentIndex(nieuw)
        self.nb.setCurrentWidget(newpage)

    def closetab(self, pagetodelete):           # werkt! (NB)
        """sluit de aangegeven tab

        bij de laatste tab: alleen leegmaken en titel generiek maken
        """
        aant = self.nb.count()
        print("closetab: deleting page", pagetodelete)
        if aant == 1:
            self.nb.setTabText(self.current, "1")
            self.nb.widget(self.current).txt.setText("")
            self.close()
        else:
            test = self.nb.widget(pagetodelete)
            print("closetab: widget is", test)
            self.nb.removeTab(pagetodelete)
            print("closetab: tab is removed")
            test.destroy()
            print("closetab: widget is destroyed")

    def revive(self, event=None):               # werkt!
        """herleef het scherm vanuit de systray
        """
        if event == gui.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
        elif event == gui.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def closeEvent(self, event=None):           # werkt!
        self.afsl()

    def afsl(self):                             # werkt!
        """applicatiedata opslaan voorafgaand aan afsluiten
        """
        self.opts["ActiveTab"] = self.nb.currentIndex()
        self.apodata = {0: self.opts}
        for i in range(self.nb.count()):
            page = self.nb.widget(i)
            title = str(self.nb.tabText(i))
            text = str(page.txt.toPlainText())
            self.apodata[i+1] = (title, text)
        self.save_notes()

    def helppage(self):                         # werkt!
        """vertoon de hulp pagina met keyboard shortcuts
        """
        self.meld(languages[self.opts["language"]]["info"])

    def meld(self, meld):                       # werkt!
        gui.QMessageBox.information(self, 'Apropos', meld, )

    def asktitle(self):                         # werkt!
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        text, ok = gui.QInputDialog.getText(self, 'Apropos',
            languages[self.opts["language"]]["ask_title"],
            gui.QLineEdit.Normal, self.nb.tabText(self.current))
        if ok:
            self.nb.setTabText(self.current, text)

    def choose_language(self):                  # werkt!
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(x, y["language"]) for x, y in languages.items()]
        cur_lng = 0
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["language"]:
                cur_lng = idx
                break
        item, ok = gui.QInputDialog.getItem(self, 'Apropos',
            languages[self.opts["language"]]["ask_language"],
            [x[1] for x in data], cur_lng, False)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == item:
                    self.opts["language"] = data[idx][0]
                    break

class Main():
    """main class van de applicatie

    de main class in apropos.py overerft hiervan
    """
    def __init__(self, log=False):
        if log:
            logging.basicConfig(filename='apropos_qt.log', level=logging.DEBUG,
                format='%(asctime)s %(message)s')
        else:
            logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(message)s')
        app = gui.QApplication(sys.argv)
        main = MainFrame()
        main.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Main(log=True)
