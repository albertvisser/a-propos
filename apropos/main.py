"""apropos_qt5.py

presentation layer and most of the application logic, Qt5 version
"""
import pathlib
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
        if not title:
            title = "A Propos"
        self.gui = gui.AproposGui(self, title=title)
        self.apofile = dml.get_apofile(fname)  # shared.get_apofile(fname)
        iconame = str(HERE / "apropos.ico")
        self.gui.set_appicon(iconame)
        self.gui.init_trayicon(iconame, tooltip="Click to revive Apropos")
        self.gui.setup_tabwidget(change_page=self.page_changed, close_page=self.closetab)
        self.gui.setup_shortcuts({'reload': (('Ctrl+R',), self.load_data),
                                  'newtab': (('Ctrl+N',), self.newtab),
                                  'close': (('Ctrl+W',), self.closetab),
                                  'hide': (('Ctrl+H',), self.hide_app),
                                  'save': (('Ctrl+S',), self.save_data),
                                  'quit': (('Ctrl+Q', 'Escape'), self.gui.close),
                                  'language': (('Ctrl+L',), self.choose_language),
                                  'next': (('Alt+Right',), self.goto_next),
                                  'prev': (('Alt+Left',), self.goto_previous),
                                  'help': (('F1',), self.helppage),
                                  'title': (('F2',), self.asktitle),
                                  'settings': (('Alt+P',), self.options)})
        self.initapp()

    def page_changed(self, event=None):
        """pagina aanpassen nadat een andere gekozen is
        """
        self.current = self.gui.get_current_page()  # (event)
        self.gui.set_focus_to_page()  # (event)

    def load_data(self):
        """get data and setup notebook
        """
        self.gui.clear_all()
        self.initapp()
        self.confirm("NotifyOnLoad", "load_text")

    def hide_app(self):
        """minimize to tray
        """
        self.confirm("AskBeforeHide", "hide_text")
        self.gui.hide_app()

    def save_data(self):
        """update persistent storage
        """
        self.afsl()
        self.confirm("NotifyOnSave", "save_text")

    def initapp(self):
        """initialiseer de applicatie
        """
        self.opts, self.apodata = dml.load_notes(self.apofile)
        if self.apodata:
            for i, x in self.apodata.items():
                self.newtab(titel=x[0], note=x[1])
            self.current = self.opts["ActiveTab"]
            self.gui.set_current_page(self.current)
        else:
            self.newtab()
            self.current = 0

    def newtab(self, titel=None, note=None):
        """initialiseer een nieuwe tab
        """
        nieuw = self.gui.get_page_count() + 1
        if not titel:
            titel = str(nieuw)
        self.gui.new_page(nieuw, titel, note)

    def goto_previous(self):
        """navigeer naar de voorgaande tab indien aanwezig
        """
        self.gui.set_previous_page()

    def goto_next(self):
        """navigeer naar de volgende tab indien aanwezig
        """
        self.gui.set_next_page()

    def closetab(self, pagetodelete=None):
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

    def helppage(self):
        """vertoon de hulp pagina met keyboard shortcuts
        """
        self.gui.meld(languages[self.opts["language"]]["info"])

    def confirm(self, setting, textitem):
        """Vraag om bevestiging (wordt afgehandeld in de dialoog)
        """
        if self.opts[setting]:
            self.gui.show_dialog(gui.CheckDialog,
                                 {'message': languages[self.opts["language"]][textitem],
                                  'option': setting,
                                  'caption': languages[self.opts["language"]]["show_text"]})
        # else:
        #     shared.log(languages[self.opts["language"]][textitem])

    def asktitle(self):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        text, ok = self.gui.get_text(prompt=languages[self.opts["language"]]["ask_title"],
                                     initial=self.gui.get_page_title(self.current))
        if ok:
            self.gui.set_page_title(self.current, text)

    def choose_language(self):
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
        self.gui.show_dialog(gui.OptionsDialog, {'sett2text': {
            'AskBeforeHide': languages[self.opts["language"]]['ask_hide'],
            'NotifyOnLoad': languages[self.opts["language"]]['notify_load'],
            'NotifyOnSave': languages[self.opts["language"]]['notify_save']}})
