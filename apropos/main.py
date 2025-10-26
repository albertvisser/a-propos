"""apropos/main.py: simple multi-tab notebooklet, application logic
"""
import pathlib
import configparser
from apropos import en
from apropos import nl
from apropos import gui
from apropos import dml

languages = {}
languages.update(en.lang)
languages.update(nl.lang)

HERE = pathlib.Path(__file__).parent  # os.path.dirname(__file__)


def apropos(fname='', title=''):
    """starts the application by calling the MainFrame class
    """
    frm = Apropos(fname=fname, title=title)
    frm.gui.go()  # sys.exit(app.exec_())


class Apropos:
    """main class voor de applicatie
    """
    def __init__(self, fname='', title=''):
        self.iconame = str(HERE / "apropos.ico")
        self.apofile = dml.get_apofile(fname)  # shared.get_apofile(fname)
        self.shortcut_data = {'reload': (('Ctrl+R',), self.load_data),
                              'newtab': (('Ctrl+N',), self.newtab),
                              'close': (('Ctrl+W',), self.closetab),
                              'hide': (('Ctrl+H',), self.hide_app),
                              'save': (('Ctrl+S',), self.save_data),
                              'quit': (('Ctrl+Q', 'Escape'), self.quit),
                              'language': (('Ctrl+L',), self.choose_language),
                              'next': (('Alt+Right',), self.goto_next),
                              'prev': (('Alt+Left',), self.goto_previous),
                              'help': (('F1',), self.helppage),
                              'title': (('F2',), self.asktitle),
                              'settings': (('Alt+P',), self.options)}
        if not title:
            title = "A Propos"
        self.gui = gui.AproposGui(self, title=title)
        self.gui.set_appicon(self.iconame)
        self.gui.init_trayicon(self.iconame, tooltip="Click to revive Apropos")
        self.gui.setup_tabwidget(change_page=self.page_changed, close_page=self.closetab)
        self.gui.setup_shortcuts(self.shortcut_data)
        self.config = configparser.ConfigParser()
        self.confpath = pathlib.Path('~/.config/a-propos/locs').expanduser()
        self.load_and_set_screenpos()
        self.initapp()

    def page_changed(self, event=None):
        """pagina aanpassen nadat een andere gekozen is
        """
        self.current = self.gui.get_current_page()  # event)
        self.gui.set_focus_to_page()  # (event)

    def quit(self, *args):
        "GUI afsluiten"
        self.gui.close()

    def load_data(self, *args):
        """get data and setup notebook
        """
        self.gui.clear_all()
        self.initapp()
        self.confirm("NotifyOnLoad", "load_text")

    def hide_app(self, *args):
        """minimize to tray
        """
        self.confirm("AskBeforeHide", "hide_text")
        self.gui.hide_app()

    def save_data(self, *args):
        """update persistent storage
        """
        self.afsl()
        self.confirm("NotifyOnSave", "save_text")

    def initapp(self):
        """initialiseer de applicatie
        """
        self.opts, self.apodata = dml.load_notes(self.apofile)
        if self.apodata:
            for x in self.apodata.values():
                self.newtab(titel=x[0], note=x[1])
            self.current = self.opts["ActiveTab"]
            self.gui.set_current_page(self.current)
        else:
            self.newtab()
            self.current = 0

    def newtab(self, event=None, titel=None, note=None):
        """initialiseer een nieuwe tab
        """
        nieuw = self.gui.get_page_count() + 1
        if not titel:
            titel = str(nieuw)
        self.gui.new_page(nieuw, titel, note)

    def goto_previous(self, *args):
        """navigeer naar de voorgaande tab indien aanwezig
        """
        self.gui.set_previous_page()

    def goto_next(self, *args):
        """navigeer naar de volgende tab indien aanwezig
        """
        self.gui.set_next_page()

    def closetab(self, event=None, pagetodelete=None):
        """sluit de aangegeven tab

        bij de laatste tab: alleen leegmaken en titel generiek maken
        """
        if not pagetodelete:
            pagetodelete = self.current
        aant = self.gui.get_page_count()
        if aant == 1:
            self.gui.clear_last_page()
            self.afsl()
            self.gui.close()
        else:
            self.gui.delete_page(pagetodelete)

    def revive(self, event=None):
        """herleef het scherm vanuit de systray
        """
        self.gui.reshow_app(event)

    def afsl(self):
        """applicatiedata opslaan (voorafgaand aan afsluiten)
        """
        apodata = {}
        self.opts["ActiveTab"] = self.gui.get_current_page()
        for i in range(self.gui.get_page_count()):
            title = self.gui.get_page_title(i)
            text = self.gui.get_page_text(i)
            apodata[i + 1] = (title, text)
        dml.save_notes(self.apofile, self.opts, apodata)
        self.get_and_save_screenpos()

    def helppage(self, *args):
        """vertoon de hulp pagina met keyboard shortcuts
        """
        self.gui.meld(languages[self.opts["language"]]["info"])

    def confirm(self, setting, textitem):
        """Vraag om bevestiging (wordt afgehandeld in de dialoog)
        """
        if self.opts[setting]:
            lang = self.opts['language']
            # ok, value = self.gui.show_dialog(SetCheck, {'message': languages[lang][textitem],
            #                                             'optionvalue': self.opts[setting],
            #                                             'caption': languages[lang]["show_text"]})
            dialogparent = SetCheck(self, message=languages[lang][textitem],
                                    optionvalue=not self.opts[setting],
                                    caption=languages[lang]["show_text"])
            ok, value = self.gui.show_dialog(dialogparent.gui)
            # if ok:  # is altijd True
            self.opts[setting] = not value

    def asktitle(self, *args):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        text, ok = self.gui.get_text(prompt=languages[self.opts["language"]]["ask_title"],
                                     initial=self.gui.get_page_title(self.current))
        if ok:
            self.gui.set_page_title(self.current, text)

    def choose_language(self, *args):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(x, y["language"]) for x, y in languages.items()]
        cur_lng = 0
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["language"]:
                cur_lng = idx
                break
        item, ok = self.gui.get_item(prompt=languages[self.opts["language"]]["ask_language"],
                                     itemlist=[x[1] for x in data],
                                     initial=cur_lng)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == item:
                    self.opts["language"] = data[idx][0]
                    break

    def options(self, event=None):
        """check settings to show various messages"""
        lang = self.opts['language']
        # self.gui.show_dialog(gui.OptionsDialog, {'sett2text': {
        # ok, result = self.gui.show_dialog(SetOptions, {'text2valuedict': {
        #     'AskBeforeHide': languages[lang]['ask_hide'],
        #     'NotifyOnLoad': languages[lang]['notify_load'],
        #     'NotifyOnSave': languages[lang]['notify_save']}})
        dialogparent = SetOptions(self, {'AskBeforeHide': languages[lang]['ask_hide'],
                                         'NotifyOnLoad': languages[lang]['notify_load'],
                                         'NotifyOnSave': languages[lang]['notify_save']})
        ok, result = self.gui.show_dialog(dialogparent.gui)
        if ok:
            for setting, value in result.items():
                self.opts[setting] = value

    def load_and_set_screenpos(self):
        "vensterpositie ophalen en instellen indien aanwezig"
        key = str(self.apofile.resolve())
        if not self.confpath.exists():
            self.config.add_section(key)
            self.set_config_values_from_screen()
            return
        with self.confpath.open() as f:
            self.config.read_file(f)
        if self.config.has_section(key):
            pos = self.config[key]['pos']
            size = self.config[key]['size']
            self.gui.set_screen_dimensions(pos, size)
        else:
            self.config.add_section(key)
            self.set_config_values_from_screen()

    def set_config_values_from_screen(self):
        "vensterpositie in config overnemen"
        key = str(self.apofile.resolve())
        pos, size = self.gui.get_screen_dimensions()
        self.config[key]['pos'] = pos
        self.config[key]['size'] = size

    def get_and_save_screenpos(self):
        "vernsterpositie uitlezen en opslaan"
        self.set_config_values_from_screen()
        with self.confpath.open('w') as f:
            self.config.write(f)


class SetOptions:
    """Toon en wijzig desgewenst instellingen
    """
    def __init__(self, parent, sett2text):  # text2valuedict):
        self.parent = parent
        self.dialog_data = {}
        self.gui = gui.OptionsDialog(self, parent.gui)
        self.controls = []
        row = 0
        # for labeltext, value in text2valuedict.items():
        for sett, text in sett2text.items():
            row += 1
            check = self.gui.add_checkbox_line_to_grid(row, text, self.parent.opts[sett])
            self.controls.append((sett, check))
        self.gui.add_buttonbox(okvalue='&Apply', cancelvalue='&Close')

    def confirm(self):
        """exchange data with caller
        """
        return {text: self.gui.get_checkbox_value(control) for text, control in self.controls}


class SetCheck:
    """Geef een melding en vraag of deze gegeven moet blijven worden
    """
    def __init__(self, parent, message, optionvalue, caption):
        self.parent = parent
        self.dialog_data = None
        self.gui = gui.CheckDialog(self, parent.gui)
        self.gui.add_label(message)
        self.check = self.gui.add_checkbox(caption, optionvalue)
        self.gui.add_ok_buttonbox()

    def confirm(self):
        "get the input before closing the dialog"
        return self.gui.get_checkbox_value(self.check)
