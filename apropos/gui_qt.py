"""apropos_qt5.py

presentation layer and most of the application logic, Qt5 version
"""
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
## import PyQt5.QtCore as core


class AproposGui(qtw.QMainWindow):
    """main class voor de applicatie
    """
    def __init__(self, master, title='Apropos'):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__(parent=None)
        # self.setWindowTitle(title)
        offset = 30 if sys.platform.startswith('win') else 10
        self.move(offset, offset)
        self.resize(650, 400)

    def set_appicon(self, iconame):
        "give the window an icon"
        self.apoicon = gui.QIcon(iconame)
        self.setWindowIcon(self.apoicon)

    def init_trayicon(self, iconame, tooltip):
        "create an icon to show in the systray"
        self.tray_icon = qtw.QSystemTrayIcon(gui.QIcon(iconame), self)
        self.tray_icon.setToolTip("Click to revive Apropos")
        ## self.tray_icon.clicked.connect(self.revive)
        ## tray_signal = "activated(QSystemTrayIcon::ActivationReason)"
        ## self.tray_icon.tray_signal.connect(self.revive)
        self.tray_icon.activated.connect(self.master.revive)
        self.tray_icon.hide()

    def setup_tabwidget(self, change_page, close_page):
        "build the container to show the tabs in"
        self.nb = qtw.QTabWidget(self)
        self.setCentralWidget(self.nb)
        self.master.current = 0
        self.nb.currentChanged.connect(change_page)
        # pagina sluiten op dubbel - of middelklik
        ## self.nb.setTabsClosable(True) # workaround: sluitgadgets
        self.nb.tabCloseRequested.connect(close_page)

    def setup_shortcuts(self, handler_dict):
        "create the app navigation"
        for label, data in handler_dict.items():
            shortcuts, handler = data
            action = qtw.QAction(label, self)
            # action.setShortcuts([x for x in shortcuts])
            action.setShortcuts(list(shortcuts))
            action.triggered.connect(handler)
            self.addAction(action)

    def go(self):
        "show the screen and start the event loop"
        self.show()
        sys.exit(self.app.exec_())

    def get_page_count(self):
        "return number of pages"
        return self.nb.count()

    def get_current_page(self, *args):
        "return selected page"
        return self.nb.currentIndex()

    def set_previous_page(self):
        "switch to previous page in the notebook"
        page_number = self.master.current - 1
        if page_number >= 0:
            self.set_current_page(page_number)

    def set_next_page(self):
        "switch to next page in the notebook"
        page_number = self.master.current + 1
        if page_number <= self.get_page_count():
            self.set_current_page(page_number)

    def set_current_page(self, page_number):
        "set selected page"
        self.nb.setCurrentIndex(page_number)

    def set_focus_to_page(self):
        "activate (bring to front) selected page"
        currentpage = self.nb.currentWidget()
        if currentpage:
            currentpage.txt.setFocus()

    def clear_all(self):
        """get data and setup notebook
        """
        aant = self.nb.count()
        widgets = [self.nb.widget(x) for x in range(aant)]
        self.nb.clear()
        for wdg in widgets:
            wdg.destroy()

    def new_page(self, nieuw, titel, note):
        """initialiseer een nieuwe tab
        """
        newpage = Page(self)
        if note is not None:
            newpage.txt.setText(note)
        self.nb.addTab(newpage, titel)
        self.nb.setCurrentIndex(nieuw)
        self.nb.setCurrentWidget(newpage)

    def clear_last_page(self):
        "clear out the last remaining tab"
        self.nb.setTabText(self.master.current, "1")
        self.nb.widget(self.master.current).txt.setText("")

    def delete_page(self, pagetodelete):
        "delete the chosen tab"
        test = self.nb.widget(pagetodelete)
        self.nb.removeTab(pagetodelete)
        test.destroy()

    def closeEvent(self, event):
        """reimplemented: event handler voor afsluiten van de applicatie
        """
        self.master.afsl()

    def hide_app(self):
        """minimize to tray
        """
        self.tray_icon.show()
        self.hide()

    def reshow_app(self, event):
        """herleef het scherm vanuit de systray
        """
        if event == qtw.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
        elif event == qtw.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def get_page_title(self, pageno):
        "paginaheader (naam in tab) ophalen"
        return str(self.nb.tabText(pageno))

    def get_page_text(self, pageno):
        "pagina tekst ophalen"
        page = self.nb.widget(pageno)
        return str(page.txt.toPlainText())

    def meld(self, meld):
        """Toon een melding in een venster
        """
        qtw.QMessageBox.information(self, 'Apropos', meld, )

    def show_dialog(self, cls, kwargs):
        """Vraag om bevestiging (wordt afgehandeld in de dialoog)
        """
        cls(self, 'Apropos', **kwargs)

    def get_text(self, prompt, initial=''):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        return qtw.QInputDialog.getText(self, 'Apropos', prompt, qtw.QLineEdit.Normal, initial)

    def set_page_title(self, pageno, title):
        "set text for tab"
        self.nb.setTabText(pageno, title)

    def get_item(self, prompt, itemlist, initial=0):
        "return choice from input dialog"
        return qtw.QInputDialog.getItem(self, 'Apropos', prompt, itemlist, initial, False)


class Page(qtw.QFrame):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent):
        super().__init__(parent)
        self.txt = qtw.QTextEdit(self)
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.txt)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class CheckDialog(qtw.QDialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option="", caption=True):
        self.parent = parent
        self.option = option
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.apoicon)
        txt = qtw.QLabel(message)
        self.check = qtw.QCheckBox(caption, self)
        self.check.setChecked(self.parent.master.opts[option])
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.exec_()

    def klaar(self):
        "(un)set the setting and close the dialog"
        self.parent.master.opts[self.option] = not self.check.isChecked()
        super().done(0)


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent, title, sett2text=None):
        self.parent = parent
        if sett2text is None:
            sett2text = {}
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.apoicon)
        vbox = qtw.QVBoxLayout()
        self.controls = []

        gbox = qtw.QGridLayout()
        col = 0
        for key, value in self.parent.master.opts.items():
            if key not in sett2text:
                continue
            col += 1
            lbl = qtw.QLabel(sett2text[key], self)
            gbox.addWidget(lbl, col, 0)
            chk = qtw.QCheckBox('', self)
            chk.setChecked(value)
            gbox.addWidget(chk, col, 1)
            self.controls.append((key, chk))
        vbox.addLayout(gbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Apply", self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton("&Close", self)
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
            self.parent.master.opts[keyvalue] = control.isChecked()
        super().accept()
