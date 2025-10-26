"""apropos/gui_qt.py: presentation layer, Qt version
"""
import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
## import PyQt6.QtCore as core


class AproposGui(qtw.QMainWindow):
    """main class voor de applicatie
    """
    def __init__(self, master, title='Apropos'):
        self.master = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__(parent=None)
        self.setWindowTitle(title)
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
        self.tray_icon.setToolTip(tooltip)  # "Click to revive Apropos")
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
            action = gui.QAction(label, self)
            # action.setShortcuts([x for x in shortcuts])
            action.setShortcuts(list(shortcuts))
            action.triggered.connect(handler)
            self.addAction(action)

    def go(self):
        "show the screen and start the event loop"
        self.show()
        sys.exit(self.app.exec())

    def get_page_count(self):
        "return number of pages"
        return self.nb.count()

    def get_current_page(self):
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

    def new_page(self, nieuw, titel, note=None):
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
        if event in (qtw.QSystemTrayIcon.ActivationReason.Unknown,
                     qtw.QSystemTrayIcon.ActivationReason.Context):
            self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
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

    # def show_dialog(self, cls, kwargs):
    def show_dialog(self, dlg):
        """Vraag om bevestiging (wordt afgehandeld in de dialoog)
        """
        # parentdlg = cls(self, 'Apropos', **kwargs)
        # result = parentdlg.gui.exec()
        result = dlg.exec()
        # return result == qtw.QDialog.StandardButton.OK, parentdlg.dialog_data
        return result == qtw.QDialog.DialogCode.Accepted, dlg.master.dialog_data

    def get_text(self, prompt, initial=''):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        return qtw.QInputDialog.getText(self, 'Apropos', prompt, text=initial)

    def set_page_title(self, pageno, title):
        "set text for tab"
        self.nb.setTabText(pageno, title)

    def get_item(self, prompt, itemlist, initial=0):
        "return choice from input dialog"
        return qtw.QInputDialog.getItem(self, 'Apropos', prompt, itemlist, initial, False)

    def set_screen_dimensions(self, pos, size):
        "vensterpositie instellen zoals aangegeven"
        x, y = (int(x) for x in pos.split('x'))
        w, h = (int(x) for x in size.split('x'))
        self.move(x, y)
        self.resize(w, h)

    def get_screen_dimensions(self):
        "uitgelezen vensterpositie teruggeven"
        # pos = self.pos()
        # size = self.rect()
        # return str(pos), str(size)
        return f'{self.x()}x{self.y()}', f'{self.width()}x{self.height()}'


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
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden

    Eventueel ook te implementeren d.m.v. QErrorMessage
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle('Apropos')
        self.setWindowIcon(parent.apoicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        # self.resize(574 + breedte, 480)

    def add_label(self, labeltext):
        """create a text on the screen
        """
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext, self))
        self.vbox.addLayout(hbox)

    def add_checkbox(self, message, value):
        """create a checkbox
        """
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox(message, self)
        check.setChecked(value)
        hbox.addWidget(check)
        self.vbox.addLayout(hbox)
        return check

    def add_ok_buttonbox(self):
        """create a button strip with handlers
        """
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)
        hbox.addWidget(ok_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.isChecked()

    def klaar(self):
        "dialoog afsluiten"
        self.master.dialog_data = self.master.confirm()
        super().accept()


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle('Apropos')
        self.setWindowIcon(self.parent.apoicon)
        self.vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox)
        self.setLayout(self.vbox)

    def add_checkbox_line_to_grid(self, row, labeltext, value):
        """create a line to turn an option on/off
        """
        lbl = qtw.QLabel(labeltext, self)
        self.gbox.addWidget(lbl, row, 0)
        chk = qtw.QCheckBox('', self)
        chk.setChecked(value)
        self.gbox.addWidget(chk, row, 1)
        return chk

    def add_buttonbox(self, okvalue, cancelvalue):
        """create a button strip with handlers
        """
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton(okvalue, self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton(cancelvalue, self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.isChecked()

    def accept(self):
        """exchange data with caller (overridden event handler)
        """
        self.master.dialog_data = self.master.confirm()
        super().accept()
