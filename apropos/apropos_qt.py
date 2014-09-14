# -*- coding: utf-8 -*-
from __future__ import print_function

import pathlib # os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import logging
from .apomixin import ApoMixin, languages
HERE = pathlib.Path(__file__).parent # os.path.dirname(__file__)

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
        show_text = languages[self.parent.opts["language"]]["show_text"]
        self.check = gui.QCheckBox(show_text, self)
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

class MainFrame(gui.QMainWindow, ApoMixin):
    """main class voor de applicatie

    subclass van Apomixin voor het gui-onafhankelijke gedeelte
    """
    def __init__(self, parent=None):
        gui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Apropos")
        offset = 30 if sys.platform.startswith('win') else 10
        self.move(offset, offset)
        self.resize(650, 400)
        self.apoicon = gui.QIcon(HERE / "apropos.ico")
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

        for label, shortcuts, handler in (
                ('reload', ('Ctrl+R',), self.load_data),
                ('newtab', ('Ctrl+N',), self.newtab),
                ('close', ('Ctrl+W',), self.closetab),
                ('hide', ('Ctrl+H',), self.hide_app),
                ('save', ('Ctrl+S',), self.save_data),
                ('quit', ('Ctrl+Q', 'Escape'), self.close),
                ('language', ('Ctrl+L',), self.choose_language),
                ('next', ('Alt+Right',), self.goto_next),
                ('prev', ('Alt+Left',), self.goto_previous),
                ('help', ('F1',), self.helppage),
                ('title', ('F2',), self.asktitle),
                ):
            action = gui.QAction(label, self)
            action.setShortcuts([x for x in shortcuts])
            self.connect(action, core.SIGNAL('triggered()'), handler)
            self.addAction(action)

        self.initapp()

    def page_changed(self, event=None):
        """pagina aanpassen nadat een andere gekozen is
        """
        n = self.nb.count()                     # doen't seem to be necessary
        self.current = self.nb.currentIndex()
        currentpage = self.nb.currentWidget()
        if currentpage:
            currentpage.txt.setFocus()

    def load_data(self):
        aant = self.nb.count()
        widgets = [self.nb.widget(x) for x in range(aant)]
        self.nb.clear()
        for wdg in widgets:
            wdg.destroy()
        self.initapp()
        self.confirm(setting="NotifyOnLoad", textitem="load_text")

    def hide_app(self):
        self.confirm(setting="AskBeforeHide", textitem="hide_text")
        self.tray_icon.show()
        self.hide()

    def save_data(self):
        self.afsl()
        self.confirm(setting="NotifyOnSave", textitem="save_text")

    def initapp(self):
        """initialiseer de applicatie
        """
        self.opts = {"AskBeforeHide": True, "ActiveTab": 0, 'language': 'eng',
            'NotifyOnSave': True, 'NotifyOnLoad': True}
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

    def newtab(self, titel=None, note=None):
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

    def goto_previous(self):
        previous = self.current - 1
        if previous < 0:
            return
        self.nb.setCurrentIndex(previous)

    def goto_next(self):
        next = self.current + 1
        if next > self.nb.count():
            return
        self.nb.setCurrentIndex(next)

    def closetab(self, pagetodelete=None):
        """sluit de aangegeven tab

        bij de laatste tab: alleen leegmaken en titel generiek maken
        """
        if pagetodelete is None:
            pagetodelete = self.current
        aant = self.nb.count()
        if aant == 1:
            self.nb.setTabText(self.current, "1")
            self.nb.widget(self.current).txt.setText("")
            self.close()
        else:
            test = self.nb.widget(pagetodelete)
            self.nb.removeTab(pagetodelete)
            test.destroy()

    def revive(self, event=None):
        """herleef het scherm vanuit de systray
        """
        if event == gui.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
        elif event == gui.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def closeEvent(self, event=None):
        self.afsl()

    def afsl(self):
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

    def helppage(self):
        """vertoon de hulp pagina met keyboard shortcuts
        """
        self.meld(languages[self.opts["language"]]["info"])

    def meld(self, meld):
        gui.QMessageBox.information(self, 'Apropos', meld, )

    def confirm(self, setting='', textitem=''):
        if self.opts[setting]:
            dlg = CheckDialog(self, 'Apropos',
                message=languages[self.opts["language"]][textitem],
                option=setting)

    def asktitle(self):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        text, ok = gui.QInputDialog.getText(self, 'Apropos',
            languages[self.opts["language"]]["ask_title"],
            gui.QLineEdit.Normal, self.nb.tabText(self.current))
        if ok:
            self.nb.setTabText(self.current, text)

    def choose_language(self):
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

def main(log=False):
    """starts the application by calling the MainFrame class
    """
    if log:
        print('with logging to file')
        logging.basicConfig(filename='apropos_qt.log', level=logging.DEBUG,
            format='%(asctime)s %(message)s')
    else:
        print('"no" logging')
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(message)s')
    app = gui.QApplication(sys.argv)
    frm = MainFrame()
    frm.show()
    sys.exit(app.exec_())
