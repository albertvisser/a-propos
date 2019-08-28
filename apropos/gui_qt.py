"""apropos_qt5.py

presentation layer and most of the application logic, Qt5 version
"""
import sys
import PyQt5.QtWidgets as QTW
import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
import apropos.shared as shared
languages = shared.languages


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


class OptionsDialog(QTW.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent):
        self.parent = parent
        sett2text = shared.get_setttexts(self.parent.opts)
        super().__init__(parent)
        self.setWindowTitle('A Propos Settings')
        vbox = QTW.QVBoxLayout()
        self.controls = []

        gbox = QTW.QGridLayout()
        col = 0
        for key, value in self.parent.opts.items():
            if key not in sett2text:
                continue
            col += 1
            lbl = QTW.QLabel(sett2text[key], self)
            gbox.addWidget(lbl, col, 0)
            chk = QTW.QCheckBox('', self)
            chk.setChecked(value)
            gbox.addWidget(chk, col, 1)
            self.controls.append((key, chk))
        vbox.addLayout(gbox)

        hbox = QTW.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = QTW.QPushButton("&Apply", self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = QTW.QPushButton("&Close", self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.exec_()

    def accept(self):
        """overridden event handler
        """
        for keyvalue, control in self.controls:
            self.parent.opts[keyvalue] = control.isChecked()
        super().accept()


class MainFrame(QTW.QMainWindow):
    """main class voor de applicatie
    """
    def __init__(self, parent=None, fname='', title=''):
        super().__init__(parent)
        if not title:
            title = "A Propos"
        self.apofile = shared.get_apofile(fname)
        self.setWindowTitle(title)
        offset = 30 if sys.platform.startswith('win') else 10
        self.move(offset, offset)
        self.resize(650, 400)
        # self.apoicon = gui.QIcon(str(HERE / "apropos.ico"))
        self.apoicon = gui.QIcon(shared.iconame)
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

        self.handlers = self.map_shortcuts_to_handlers()
        for label, shortcuts in shared.get_shortcuts():
            handler = self.handlers[label]
            action = QTW.QAction(label, self)
            action.setShortcuts([x for x in shortcuts])
            action.triggered.connect(handler)
            self.addAction(action)

        self.initapp()

    def map_shortcuts_to_handlers(self):
        "because we cannot import the handlers from shared"
        return {'reload': self.load_data,
                'newtab': self.newtab,
                'close': self.closetab,
                'hide': self.hide_app,
                'save': self.save_data,
                'quit': self.close,
                'language': self.choose_language,
                'next': self.goto_next,
                'prev': self.goto_previous,
                'help': self.helppage,
                'title': self.asktitle,
                'settings': self.options}

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
        self.opts, self.apodata = shared.load_notes(self.apofile)
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
        shared.save_notes(self.apofile, apodata)

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
            shared.log(languages[self.opts["language"]][textitem])

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

    def options(self, event=None):
        """check settings to show various messages"""
        OptionsDialog(self)


def main(fname='', title=''):
    """starts the application by calling the MainFrame class
    """
    print('in qt version')
    app = QTW.QApplication(sys.argv)
    frm = MainFrame(fname=fname, title=title)
    frm.show()
    sys.exit(app.exec_())
