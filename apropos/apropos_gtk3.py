"""apropos_gtk3.py

presentation layer and most of the application logic, gtk3 version
"""
import os
import pathlib
import sys
import logging
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from .apomixin import ApoMixin, languages
HERE = pathlib.Path(__file__).parent
LOGDIR = HERE.parent / 'logs' / pathlib.Path.cwd().name
if not LOGDIR.exists():
    LOGDIR.mkdir()
logging.basicConfig(filename=str(LOGDIR / 'apropos_gtk3.log'),
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def log(message):
    "only log when DEBUG is set in environment"
    if 'DEBUG' in os.environ and os.environ["DEBUG"] != "0":
        logging.info(message)


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
    def __init__(self, parent, title, message="", option=""):
        self._parent = parent
        self.option = option
        super().__init__(title, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()
        box.add(Gtk.Label(message))
        show_text = languages[self._parent.opts["language"]]["show_text"]
        self.check = Gtk.CheckButton.new_with_label(show_text)
        box.add(self.check)
        self.show_all()


class MainFrame(Gtk.Application):
    """main class voor de applicatie
    """
    def __init__(self, file='', title=''):
        super().__init__()
        self.file = file
        self.title = title

    def do_activate(self):
        """start GUI
        """
        win = MainWin(application=self, file=self.file, title=self.title)
        win.present()

    def close(self, action, param):
        """end GUI
        """
        self.quit()


class MainWin(Gtk.ApplicationWindow, ApoMixin):
    """main window voor de applicatie

    subclass van Apomixin voor het gui-onafhankelijke gedeelte
    """
    def __init__(self, application, file='', title=''):
        if not title:
            title = "A Propos"
        self.app = application
        Gtk.ApplicationWindow.__init__(self, application=application, title=title)
        ApoMixin.__init__(self)
        self.set_apofile(file)
        offset = 30 if sys.platform.startswith('win') else 10
        self.move(offset, offset)
        self.resize(650, 400)
        self.apoicon = str(HERE / "apropos.ico")
        self.set_icon_from_file(self.apoicon)
        # let's not do this feature yet
        ## self.tray_icon = Gtk.StatusIcon.new_from_file(self.apoicon)
        ## self.tray_icon.set_tooltip_text("Click to revive Apropos")
        ## self.tray_icon.connect('activate', self.revive)
        ## self.tray_icon.set_visible(False)

        self.nb = Gtk.Notebook()
        self.nb.set_scrollable(True)
        self.add(self.nb)
        self.current = 0
        self.nb.connect('switch-page', self.page_changed)
        # pagina sluiten op dubbel - of middelklik
        ## self.nb.setTabsClosable(True) # workaround: sluitgadgets

        for label, shortcuts, handler in (
                ('reload', ('<Control>r',), self.load_data),
                ('newtab', ('<Control>n',), self.newtab),
                ('close', ('<Control>w',), self.closetab),
                ## ('hide', ('<Control>h',), self.hide_app),                # TODO
                ('save', ('<Control>s',), self.save_data),
                ('quit', ('<Control>q', 'Escape'), self.close),
                ('language', ('<Control>l',), self.choose_language),
                ('next', ('<Alt>Right',), self.goto_next),
                ('prev', ('<Alt>Left',), self.goto_previous),
                ('help', ('F1',), self.helppage),
                ('title', ('F2',), self.asktitle), ):
            action = Gio.SimpleAction.new(label, None)
            action.connect("activate", handler)
            for accel in shortcuts:
                print(accel)
                self.add_action(action)
                self.app.add_accelerator(accel, 'win.' + label, None)

        self.initapp()
        self.nb.show()

    def page_changed(self, nb, page, page_num):
        """pagina aanpassen nadat een andere gekozen is
        """
        # page en page_num is blijkbaar de pagina waar we naartoe gaan
        # terwijl get_current_page de pagina aangeeft waar we vandaan komen
        self.current = page_num
        self.currentpage = page
        print('page changed:', self.current)
        if self.currentpage:
            self.currentpage.txt.grab_focus()

    def load_data(self, *args):
        """get data and setup notebook
        """
        aant = len(self.nb)
        for i in reversed(range(aant)):
            self.nb.remove_page(i - 1)
        self.initapp()
        self.confirm(setting="NotifyOnLoad", textitem="load_text")

    def hide_app(self, *args):          # TODO: test
        """minimize to tray
        """
        self.confirm(setting="AskBeforeHide", textitem="hide_text")
        self.tray_icon.set_visible(True)    # niet gedefinieerd
        self.hide()

    def save_data(self, *args):
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
            self.nb.set_current_page(self.current)
        else:
            self.newtab()
            self.current = 0

    def newtab(self, *args, titel=None, note=None):
        """initialiseer een nieuwe tab
        """
        aant = len(self.nb)
        if not titel:
            titel = str(aant + 1)
        newpage = Page(self)
        if note is not None:
            newpage.textbuffer.set_text(note)
        else:
            newpage.textbuffer.set_text("")
        self.nb.append_page(newpage, Gtk.Label(titel))
        self.nb.set_current_page(aant)

    def goto_previous(self, *args):
        """navigeer naar de voorgaande tab indien aanwezig
        """
        print('goto_previous called')
        ## newtab = self.current - 1
        ## if newtab < 0:
            ## return
        ## self.nb.set_current_page(newtab)
        self.nb.prev_page()

    def goto_next(self, *args):
        """navigeer naar de volgende tab indien aanwezig
        """
        print('goto_next called')
        ## newtab = self.current + 1
        ## if newtab > len(self.nb):
            ## return
        ## self.nb.set_current_page(newtab)
        self.nb.next_page()

    def closetab(self, *args, pagetodelete=None):
        """sluit de aangegeven tab

        bij de laatste tab: alleen leegmaken en titel generiek maken
        """
        print('_closetab called with', len(self.nb), 'tabs')
        print('  on tab', pagetodelete)
        if not pagetodelete:
            pagetodelete = self.current
            print('  pagetodelete is now', pagetodelete)
        aant = len(self.nb)
        if aant == 1:
            curpage = self.nb.get_nth_page(0)
            self.nb.set_tab_label_text(curpage, "1")
            curpage.textbuffer.set_text("")
            self.close()
        else:
            ## test = self.nb.get_nth_page(pagetodelete)
            self.nb.remove_page(pagetodelete)

    def revive(self, *args):           # TODO: test
        """herleef het scherm vanuit de systray
        """
        ## if event == QTW.QSystemTrayIcon.Unknown:
            ## self.tray_icon.showMessage('Apropos', "Click to revive Apropos")
        ## elif event == QTW.QSystemTrayIcon.Context:
            ## pass
        ## else:
        self.show()
        self.tray_icon.set_visible(False)  # niet gedefinieerd

    def close(self, *args):
        self.afsl()
        if args:
            self.app.close(*args)
        else:
            self.app.close(None, None)

    def afsl(self):
        """applicatiedata opslaan voorafgaand aan afsluiten
        """
        self.opts["ActiveTab"] = self.current
        apodata = {0: self.opts}
        for i in range(len(self.nb)):
            page = self.nb.get_nth_page(i)
            title = self.nb.get_tab_label_text(page)
            text = page.textbuffer.get_text(page.textbuffer.get_start_iter(),
                                            page.textbuffer.get_end_iter(),
                                            True)
            apodata[i + 1] = (title, text)
        print(apodata)
        self.save_notes(apodata)

    def helppage(self, *args):
        """vertoon de hulp pagina met keyboard shortcuts
        """
        self.meld(languages[self.opts["language"]]["info"])

    def meld(self, meld):
        """Toon een melding in een venster
        """
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, meld)
        ## dialog.format_secondary_text(
            ## "And this is the secondary text that explains things.")
        dialog.run()
        dialog.destroy()

    def confirm(self, setting='', textitem=''):
        """Vraag om bevestiging (wordt afgehandeld in de dialoog)
        """
        if self.opts[setting]:
            dlg = CheckDialog(self, 'Apropos',
                              message=languages[self.opts["language"]][textitem],
                              option=setting)
            response = dlg.run()
            if response == Gtk.ResponseType.OK:
                if dlg.check.get_active():
                    self.opts[setting] = False
            dlg.destroy()

    def asktitle(self, *args):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        text = self.nb.get_tab_label_text(self.currentpage)
        dlg = InputDialog(self, 'Apropos')
        dlg.get_text(caption=languages[self.opts["language"]]["ask_title"],
                     text=text)
        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            text = dlg.input.get_text()
            self.nb.set_tab_label_text(self.currentpage, text)
        dlg.destroy()

    def choose_language(self, *args):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        print('choose_language called')
        data = [(x, y["language"]) for x, y in languages.items()]
        cur_lng = 0
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["language"]:
                cur_lng = idx
                break
        dlg = InputDialog(self, 'Apropos')
        dlg.get_item(caption=languages[self.opts["language"]]["ask_language"],
                     items=[x[1] for x in data],
                     default=cur_lng)
        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            text = dlg.input.get_active_text()
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == text:
                    self.opts["language"] = data[idx][0]
                    break
        dlg.destroy()


def main(file='', title=''):
    """starts the application by calling the MainFrame class
    """
    app = MainFrame(file=file, title=title)
    ## win = MainFrame(app, file=file, title=title)
    ## win.connect("delete-event", Gtk.main_quit)
    ## win.show_all()
    app.run(sys.argv)
    ## Gtk.main()
