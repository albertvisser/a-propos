"""apropos_gtk3.py: presentation layer, gtk3 version

unfortunately gtk appears not to let me do this the way I want it to:
this creates an empty window with working accelerators that crashes when I try to close it
"""
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


def convert2gtk(accel):
    "rebuild the accel string in gtk format"
    parts = accel.split('+')
    for ix, part in enumerate(parts[:-1]):
        parts[ix] = part.replace('ctrl', 'Control').join(('<', '>'))
    if len(parts[-1]) == 1:
        parts[-1] = parts[-1].upper()
    accel = ''.join(parts)
    return accel


class AproposGui(Gtk.Application):
    """main class voor de applicatie
    """
    def __init__(self, master, title=''):
        # breakpoint()
        super().__init__()
        self.master = master
        self.title = title

    def do_activate(self):
        """start GUI
        """
        self.win = MainWin(application=self, title=self.title)
        self.win.present()

    def close(self, action, param):
        """end GUI
        """
        self.quit()

    def set_appicon(self, iconame):
        """API-compliance: gtk requires this to be done in the application window's __init__"""

    def init_trayicon(self, iconame, tooltip):
        """API-compliance: gtk requires this to be done in the application window's __init__"""

    def setup_tabwidget(self, change_page, close_page):
        """API-compliance: gtk requires this to be done in the application window's __init__"""

    def setup_shortcuts(self, shortcut_dict):
        """API-compliance: gtk requires this to be done in the application window's __init__"""

    def go(self):
        """API-compliance: # gtk starts the event loop before creating the application window"""
        print(f"in AproposGui.go, {hasattr(self, 'win')=}")
        self.run()
        print(f"in AproposGui.go, {hasattr(self, 'win')=}")

    def get_page_count(self):
        "relay to application window"
        if hasattr(self, 'win'):
            return self.win.get_page_count()
        print(f'in AproposGui.get_page_count, window not created yet')
        return 0

    def get_current_page(self):
        "relay to application window"
        if hasattr(self, 'win'):
            return self.win.get_current_page()

    def set_previous_page(self):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.set_previous_page()

    def set_next_page(self):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.set_next_page()

    def set_current_page(self, pageno):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.set_current_page(pageno)

    def set_focus_to_page(self):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.set_focus_to_page()

    def clear_all(self):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.clear_all()

    def new_page(self, nieuw, titel, text):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.new_page(nieuw, titel, text)
            print(f'in AproposGui.new_page, creating page {nieuw}')
        else:
            print(f'in AproposGui.new_page, window not created yet')

    def clear_last_page(self):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.clear_last_page()

    def delete_page(self, pagetodelete):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.delete_page(pagetodelete)

    def hide_app(self):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.hide_app()

    def reshow_app(self, event):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.reshow_app(event)

    def get_page_title(self, pageno):
        "relay to application window"
        if hasattr(self, 'win'):
            return self.win.get_page_title(pageno)

    def get_page_text(self, pageno):
        "relay to application window"
        return self.win.get_page_text(pageno)

    def meld(self, meld):
        """Toon een melding in een venster
        """
        if hasattr(self, 'win'):
            dialog = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, meld)
            ## dialog.format_secondary_text(
                ## "And this is the secondary text that explains things.")
            dialog.run()
            dialog.destroy()

    def show_dialog(self, cls, kwargs):  # (om CheckDialog en OptionsDialog heen)
        if hasattr(self, 'win'):
            dlg = cls(self.win, **kwargs)
            # dlg = CheckDialog(self, 'Apropos', message=languages[self.opts["language"]][textitem],
            #                   option=setting)
            # dlg = OptionsDialog(self)
            response = dlg.run()
            if response == Gtk.ResponseType.OK:
                dlg.accept()
            dlg.destroy()

    def get_text(self, prompt, initial=''):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.get_text(prompt, initial='')

    def set_page_title(self, pageno, title):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.set_page_title(pageno, title)

    def get_item(self, prompt, itemlist, initial=0):
        "relay to application window"
        if hasattr(self, 'win'):
            self.win.get_item(prompt, itemlist, initial=0)

    def set_screen_dimensions(self, pos, size):
        "vensterpositie instellen zoals aangegeven"
        if hasattr(self, 'win'):
            x, y = (int(x) for x in pos.split('x'))
            w, h = (int(x) for x in size.split('x'))
            self.app.win.move(x, y)
            self.app.win.resize(w, h)

    def get_screen_dimensions(self):
        "uitgelezen vensterpositie teruggeven"
        if hasattr(self, 'win'):
            x, y = self.app.win.get_position()
            w, h = self.app.win.get_height()
            return f'{x}x{y}', f'{w}x{h}'


class MainWin(Gtk.ApplicationWindow):
    """main window voor de applicatie
    """
    def __init__(self, application, title=''):
        if not title:
            title = "A Propos"
        self.app = application
        Gtk.ApplicationWindow.__init__(self, application=application, title=title)
        offset = 30 if sys.platform.startswith('win') else 10
        self.move(offset, offset)
        self.resize(650, 400)
        # originally planned to be done from the Apropos class in main.py, but gtk won't let me
        self.set_appicon(self.app.master.iconame)
        self.init_trayicon(self.app.master.iconame, tooltip='Click to revive Apropos')
        self.setup_tabwidget(change_page=self.app.master.page_changed,
                             close_page=self.app.master.closetab)
        self.setup_shortcuts(self.app.master.shortcut_data)
        self.app.master.initapp()

    def set_appicon(self, iconame):
        self.apoicon = iconame
        self.set_icon_from_file(self.apoicon)

    def init_trayicon(self, iconame, tooltip):
        'minimize to tray nog even niet geïmplementeerd'
        # let's not do this feature yet
        ## self.tray_icon = Gtk.StatusIcon.new_from_file(self.apoicon)
        ## self.tray_icon.set_tooltip_text("Click to revive Apropos")
        ## self.tray_icon.connect('activate', self.revive)
        ## self.tray_icon.set_visible(False)

    def setup_tabwidget(self, change_page, close_page):
        # changepage_callback verwijst naar een methode op de klasse uit main.py met als inhoud:
        #     self.current = self.gui.get_current_page()  # event)
        #     self.gui.set_focus_to_page()  # (event)
        # terwijl ik hier ga connecten aan een methode van het applicatiewindow
        self.nb = Gtk.Notebook()
        self.nb.set_scrollable(True)
        self.add(self.nb)
        self.current = 0
        self.nb.connect('switch-page', self.page_changed)
        self.nb.show()
        # pagina sluiten op dubbel - of middelklik
        ## self.nb.setTabsClosable(True) # workaround: sluitgadgets

    def page_changed(self, nb, page, page_num):
        """pagina aanpassen nadat een andere gekozen is
        """
        # page en page_num is blijkbaar de pagina waar we naartoe gaan
        # terwijl get_current_page de pagina aangeeft waar we vandaan komen
        self.current = page_num
        self.currentpage = page
        if self.currentpage:
            self.currentpage.txt.grab_focus()

    def setup_shortcuts(self, shortcut_dict):
        for label, data in shortcut_dict.items():
            if label == 'hide':
                continue            # TODO: make hiding in tray possible
            accels, handler = data
            action = Gio.SimpleAction.new(label, None)
            action.connect("activate", handler)
            self.add_action(action)
            for accel in accels:
                self.app.add_accelerator(convert2gtk(accel), 'win.' + label, None)

    def get_page_count(self):
        return len(self.nb)

    def get_current_page(self):
        return self.current

    def set_previous_page(self):
        self.nb.prev_page()

    def set_next_page(self):
        self.nb.next_page()

    def set_current_page(self, pageno):
        self.nb.set_current_page(pageno)
        self.current = pageno

    def set_focus_to_page(self):
        ...

    def clear_all(self):
        aant = len(self.nb)
        for i in reversed(range(aant)):
            self.nb.remove_page(i - 1)

    def new_page(self, nieuw, titel, note):
        newpage = Page(self)
        if note is not None:
            newpage.textbuffer.set_text(note)
        else:
            newpage.textbuffer.set_text("")
        self.nb.append_page(newpage, Gtk.Label(titel))
        aant = self.get_page_count() + 1
        self.set_current_page(aant)

    def clear_last_page(self):
        curpage = self.nb.get_nth_page(0)
        self.nb.set_tab_label_text(curpage, "1")
        curpage.textbuffer.set_text("")

    def delete_page(self, pagetodelete):
        self.nb.remove_page(pagetodelete)

    def hide_app(self):
        "minimize to tray"
        # self.tray_icon.set_visible(True)    # niet gedefinieerd
        # self.hide()

    def reshow_app(self, event):
        """herleef het scherm vanuit de systray
        """
        ## if event == QTW.QSystemTrayIcon.Unknown:
            ## self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
        ## elif event == QTW.QSystemTrayIcon.Context:
            ## pass
        ## else:
        # self.show()
        # self.tray_icon.set_visible(False)  # niet gedefinieerd

    def get_page_title(self, pageno):
        page = self.nb.get_nth_page(pageno)
        return self.nb.get_tab_label_text(page)

    def get_page_text(self, pageno):
        page = self.nb.get_nth_page(pageno)
        return page.textbuffer.get_text(page.textbuffer.get_start_iter(),
                                        page.textbuffer.get_end_iter(),
                                        True)

    def get_text(self, prompt, initial=''):  #  (subdialog voor page title)
        text = self.nb.get_tab_label_text(self.currentpage)
        dlg = InputDialog(self, 'Apropos')
        # dlg.get_text(caption=languages[self.opts["language"]]["ask_title"], text=text)
        dlg.get_text(caption=prompt, text=text)
        response = dlg.run()
        text = dlg.input.get_text()
        ok = response == Gtk.ResponseType.OK
        dlg.destroy()
        return text, ok

    def set_page_title(self, pageno, text):
        # self.nb.set_tab_label_text(self.currentpage, text)
        self.nb.set_tab_label_text(pageno, text)

    def get_item(self, prompt, itemlist, initial=0):  #  (subdialog voor language)
        dlg = InputDialog(self, 'Apropos')
        dlg.get_item(caption=prompt,  # languages[self.opts["language"]]["ask_language"],
                     items=[x[1] for x in itemlist],
                     default=initial)
        response = dlg.run()
        ok = response == Gtk.ResponseType.OK
        text = dlg.input.get_active_text()
        dlg.destroy()
        return text, ok

    def close(self, *args):
        if args:
            self.app.close(*args)
        else:
            self.app.close(None, None)


class Page(Gtk.Frame):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent):
        super().__init__()
        self.set_border_width(10)
        grid = Gtk.Grid()

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.txt = Gtk.TextView()
        self.textbuffer = self.txt.get_buffer()
        self.txt.set_editable(True)
        self.txt.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolledwindow.add(self.txt)
        self.add(grid)
        self.show_all()


class CheckDialog(Gtk.Dialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option="", caption=""):
        self._parent = parent
        self.option = option
        super().__init__(title, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()
        box.add(Gtk.Label(message))
        # show_text = languages[self._parent.opts["language"]]["show_text"]
        self.check = Gtk.CheckButton.new_with_label(caption)  # show_text)
        box.add(self.check)
        self.show_all()

    def accept(self):
        "on pressing Ok: communicate changed setting back to parent"
        if self.check.get_active():
            self.parent.opts[self.option] = False


class OptionsDialog(Gtk.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent, sett2text):
        self.parent = parent
        super().__init__('A Propos Settings', parent, 0,
                         (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                          Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        box = self.get_content_area()
        grid = Gtk.Grid()
        grid.set_column_spacing(15)
        self.controls = []
        row = -1
        # for key, value in self.parent.opts.items():
        #     if key not in sett2text:
        #         continue
        for key in sett2text:
            value = self.parent.opts.items[key]
            row += 1
            grid.attach(Gtk.Label(sett2text[key]), 0, row, 1, 1)
            chk = Gtk.CheckButton.new_with_label('')
            chk.set_active(value)
            grid.attach(chk, 1, row, 1, 1)
            self.controls.append((key, chk))
        box.add(grid)
        self.show_all()

    def accept(self):
        "on pressing Ok: communicate changed settings back to parent"
        for keyvalue, control in self.controls:
            self.parent.opts[keyvalue] = control.get_active()


class InputDialog(Gtk.Dialog):
    "dialog for getting text input"
    def __init__(self, parent, title=""):
        super().__init__(title, parent, 0,
                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                          Gtk.STOCK_OK, Gtk.ResponseType.OK))

    def get_text(self, title="", caption="Enter some text", text=""):
        """callback for text field
        """
        self.input = Gtk.Entry()
        if text:
            self.input.set_text(text)

        box = self.get_content_area()
        box.add(Gtk.Label(caption))
        box.add(self.input)
        self.show_all()

    def get_item(self, title="", caption="Choose an item", items=None, default=0):
        """callback for selection field (combobox)
        """
        if not items:
            items = []
        self.input = Gtk.ComboBoxText()
        for text in items:
            self.input.append_text(text)
        self.input.set_active(default)

        box = self.get_content_area()
        box.add(Gtk.Label(caption))
        box.add(self.input)
        self.show_all()
