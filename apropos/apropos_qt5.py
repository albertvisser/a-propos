"""apropos_qt5.py

presentation layer and most of the application logic, Qt5 version
"""
import os
import pathlib
import sys
import logging
import PyQt5.QtWidgets as QTW
import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
from .apomixin import ApoMixin, languages
HERE = pathlib.Path(__file__).parent  # os.path.dirname(__file__)
LOGFILE = HERE.parent / 'logs' / 'apropos_qt.log'
WANT_LOGGING = 'DEBUG' in os.environ and os.environ["DEBUG"] != "0"
if WANT_LOGGING:
    LOGFILE.parent.mkdir(exist_ok=True)
    LOGFILE.touch(exist_ok=True)
    logging.basicConfig(filename=str(LOGFILE),
                        level=logging.DEBUG, format='%(asctime)s %(message)s')


def log(message):
    "only log when DEBUG is set in environment"
    if WANT_LOGGING:
        logging.info(message)


class Page(QTW.QFrame):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent):
        super().__init__(parent)
        self.txt = QTW.QTextEdit(self)
        vbox = QTW.QVBoxLayout()
        hbox = QTW.QHBoxLayout()
        hbox.addWidget(self.txt)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class CheckDialog(QTW.QDialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option=""):
        self.parent = parent
        self.option = option
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.apoicon)
        txt = QTW.QLabel(message)
        show_text = languages[self.parent.opts["language"]]["show_text"]
        self.check = QTW.QCheckBox(show_text, self)
        ok_button = QTW.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)
        vbox = QTW.QVBoxLayout()

        hbox = QTW.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = QTW.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = QTW.QHBoxLayout()
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
        super().done(0)


class MainFrame(QTW.QMainWindow, ApoMixin):
    """main class voor de applicatie

    subclass van Apomixin voor het gui-onafhankelijke gedeelte
    """
    def __init__(self, parent=None, file='', title=''):
        super().__init__(parent)
        if not title:
            title = "A Propos"
        self.set_apofile(file)
        self.setWindowTitle(title)
        offset = 30 if sys.platform.startswith('win') else 10
        self.move(offset, offset)
        self.resize(650, 400)
        self.apoicon = gui.QIcon(str(HERE / "apropos.ico"))
        self.setWindowIcon(self.apoicon)
        self.tray_icon = QTW.QSystemTrayIcon(self.apoicon, self)
        self.tray_icon.setToolTip("Click to revive Apropos")
        ## self.tray_icon.clicked.connect(self.revive)
        ## tray_signal = "activated(QSystemTrayIcon::ActivationReason)"
        ## self.tray_icon.tray_signal.connect(self.revive)
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        self.nb = QTW.QTabWidget(self)
        self.setCentralWidget(self.nb)
        self.current = 0
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
                ('title', ('F2',), self.asktitle), ):
            action = QTW.QAction(label, self)
            action.setShortcuts([x for x in shortcuts])
            action.triggered.connect(handler)
            self.addAction(action)

        self.initapp()

    def page_changed(self):  # , event=None):
        """pagina aanpassen nadat een andere gekozen is
        """
        self.current = self.nb.currentIndex()
        currentpage = self.nb.currentWidget()
        if currentpage:
            currentpage.txt.setFocus()

    def load_data(self):
        """get data and setup notebook
        """
        aant = self.nb.count()
        widgets = [self.nb.widget(x) for x in range(aant)]
        self.nb.clear()
        for wdg in widgets:
            wdg.destroy()
        self.initapp()
        self.confirm(setting="NotifyOnLoad", textitem="load_text")

    def hide_app(self):
        """minimize to tray
        """
        self.confirm(setting="AskBeforeHide", textitem="hide_text")
        self.tray_icon.show()
        self.hide()

    def save_data(self):
        """update persistent storage
        """
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
        if not titel:
            titel = str(nieuw)
        newpage = Page(self)
        if note is not None:
            newpage.txt.setText(note)
        self.nb.addTab(newpage, titel)
        self.nb.setCurrentIndex(nieuw)
        self.nb.setCurrentWidget(newpage)

    def goto_previous(self):
        """navigeer naar de voorgaande tab indien aanwezig
        """
        newtab = self.current - 1
        if newtab < 0:
            return
        self.nb.setCurrentIndex(newtab)

    def goto_next(self):
        """navigeer naar de volgende tab indien aanwezig
        """
        newtab = self.current + 1
        if newtab > self.nb.count():
            return
        self.nb.setCurrentIndex(newtab)

    def closetab(self, pagetodelete=None):
        """sluit de aangegeven tab

        bij de laatste tab: alleen leegmaken en titel generiek maken
        """
        if not pagetodelete:
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
        if event == QTW.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
        elif event == QTW.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def closeEvent(self, event=None):
        """reimplemented: event handler voor afsluiten van de applicatie
        """
        self.afsl()

    def afsl(self):
        """applicatiedata opslaan voorafgaand aan afsluiten
        """
        self.opts["ActiveTab"] = self.nb.currentIndex()
        apodata = {0: self.opts}
        for i in range(self.nb.count()):
            page = self.nb.widget(i)
            title = str(self.nb.tabText(i))
            text = str(page.txt.toPlainText())
            apodata[i + 1] = (title, text)
        self.save_notes(apodata)

    def helppage(self):
        """vertoon de hulp pagina met keyboard shortcuts
        """
        self.meld(languages[self.opts["language"]]["info"])

    def meld(self, meld):
        """Toon een melding in een venster
        """
        QTW.QMessageBox.information(self, 'Apropos', meld, )

    def confirm(self, setting='', textitem=''):
        """Vraag om bevestiging (wordt afgehandeld in de dialoog)
        """
        if self.opts[setting]:
            CheckDialog(self, 'Apropos',
                        message=languages[self.opts["language"]][textitem],
                        option=setting)
        else:
            logging.info(languages[self.opts["language"]][textitem])

    def asktitle(self):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        text, ok = QTW.QInputDialog.getText(
            self, 'Apropos', languages[self.opts["language"]]["ask_title"],
            QTW.QLineEdit.Normal, self.nb.tabText(self.current))
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
        item, ok = QTW.QInputDialog.getItem(
            self, 'Apropos', languages[self.opts["language"]]["ask_language"],
            [x[1] for x in data], cur_lng, False)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == item:
                    self.opts["language"] = data[idx][0]
                    break


def main(file='', title=''):
    """starts the application by calling the MainFrame class
    """
    app = QTW.QApplication(sys.argv)
    frm = MainFrame(file=file, title=title)
    frm.show()
    sys.exit(app.exec_())
