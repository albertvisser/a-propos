"""apropos_wx.py

presentation layer and most of the application logic, wxPython (Phoenix) version
"""
from __future__ import print_function
try:
    import pathlib  # os
except ImportError:
    import pathlib2 as pathlib
## import sys
import wx
import wx.adv
from .apomixin import ApoMixin, languages
HERE = pathlib.Path(__file__).parent  # os.path.dirname(__file__)
DFLT_SIZE = (650, 400)


class Page(wx.Panel):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent, id, mf):
        wx.Panel.__init__(self, parent, id)
        self.txt = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=DFLT_SIZE)
        # self.txt.Bind(wx.EVT_KEY_DOWN, mf.on_key)
        ## self.Bind(wx.EVT_TEXT, self.OnEvtText, self.txt)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        # sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(self.txt, 1, wx.EXPAND | wx.ALL, 10)
        # sizer0.Add(sizer1, 1, wx.EXPAND)
        self.SetSizer(sizer0)
        # self.SetAutoLayout(True)
        # sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        self.Layout()


class CheckDialog(wx.Dialog):
    """Dialog die kan worden ingesteld om niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, id, title, size=(-1, 120), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, message=""):
        self.parent = parent
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        pnl = self  # wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl, -1, message), 1, wx.ALL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.check = wx.CheckBox(pnl, -1,
                                 languages[self.parent.opts["language"]]["show_text"])
        sizer1.Add(self.check, 0, wx.EXPAND)
        sizer0.Add(sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, id=wx.ID_OK)
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        ## sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    sett2text = {'AskBeforeHide': 'Melden dat de applicatie verborgen wordt in de system tray',
                 'NotifyOnLoad': 'Melden dat de data opnieuw opgehaald is',
                 'NotifyOnSave': 'Melden dat de data opgeslagen is'}

    def __init__(self, parent, id):
        self.parent = parent
        super().__init__(parent, id, title='A Propos settings voor meldingen')
        pnl = self  # wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.FlexGridSizer(cols=2)
        self.controls = []
        for key, value in self.parent.opts.items():
            if key not in self.sett2text:
                continue
            sizer1.Add(wx.StaticText(pnl, -1, self.sett2text[key]), 1, wx.ALL, 5)
            chk = wx.CheckBox(self, -1, '')
            chk.SetValue(value)
            sizer1.Add(chk, 1, wx.ALL, 5)
            self.controls.append((key, chk))
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, id=wx.ID_APPLY)
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_APPLY)
        btn = wx.Button(pnl, id=wx.ID_CLOSE)
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        # sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()


class MainFrame(wx.Frame, ApoMixin):
    """main class voor de applicatie

    subclass van Apomixin voor het gui-onafhankelijke gedeelte
    """
    def __init__(self, parent, fname, title, id=-1):
        title = title or 'Apropos'
        self.quitting = False
        wx.Frame.__init__(self, parent, id, title=title, pos=(10, 10))  # , size=DFLT_SIZE)
        self.apoicon = wx.Icon(str(HERE / "apropos.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.apoicon)
        pnl = self  # wx.Panel(self, -1)
        self.nb = wx.Notebook(pnl, -1)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.page_changed)
        self.nb.Bind(wx.EVT_LEFT_DCLICK, self.on_left_doubleclick)
        self.nb.Bind(wx.EVT_MIDDLE_DOWN, self.on_left_doubleclick)
        accel_list = []
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
                ('settings', ('Alt+P',), self.options), ):
            menuitem = wx.MenuItem(None, -1, label)
            self.Bind(wx.EVT_MENU, handler, menuitem)
            for key in shortcuts:
                accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
                ok = accel.FromString(key)
                if ok:
                    accel_list.append(accel)
        accel_table = wx.AcceleratorTable(accel_list)
        self.SetAcceleratorTable(accel_table)
        self.set_apofile(fname)
        self.initapp()
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        # sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(self.nb, 1, wx.EXPAND)  # | wx.ALL, 10)
        # sizer0.Add(sizer1, 1, wx.EXPAND)
        pnl.SetSizer(sizer0)
        # pnl.SetAutoLayout(True)
        # sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        # pnl.Layout()
        self.Bind(wx.EVT_CLOSE, self.close)
        self.Show()

    def page_changed(self, event=None):
        """pagina aanpassen nadat een andere gekozen is
        """
        if not self.quitting:
            self.current = event.GetSelection()
            currentpage = self.nb.GetPage(self.current)
            currentpage.txt.SetFocus()
            event.Skip()

    def on_left_doubleclick(self, event=None):
        """reageert op dubbelklikken op tab t.b.v. verwijderen pagina
        """
        print('in mainframe.on_left_doubleclick')
        x = event.GetX()
        y = event.GetY()
        item, _ = self.nb.HitTest((x, y))
        print('    event item is', item)
        self.closetab(item)
        event.Skip()

    def load_data(self, event=None):
        """get data and setup notebook
        """
        print('in load_data')
        self.quitting = True  # bypass page_changed handling
        self.nb.DeleteAllPages()
        self.quitting = not self.quitting
        # self.oldopts = self.opts   # settings veiligstellen
        self.initapp()
        # self.opts.update({x: y for x, y in self.oldopts.items() if x != 'ActiveTab'})
        self.confirm(setting="NotifyOnLoad", textitem="load_text")

    def hide_app(self, event=None):
        """minimize to tray
        """
        self.confirm(setting="AskBeforeHide", textitem="hide_text")
        self.tbi = wx.adv.TaskBarIcon()
        self.tbi.SetIcon(self.apoicon, "Click to revive Apropos")
        self.tbi.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.revive)
        self.tbi.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.revive)
        self.Hide()

    def save_data(self, event=None):
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
            self.nb.ChangeSelection(self.opts["ActiveTab"])
            self.current = self.opts["ActiveTab"]
        else:
            self.newtab()
            self.current = 0

    def newtab(self, event=None, titel=None, note=None):
        """initialiseer een nieuwe tab
        """
        nieuw = self.nb.GetPageCount()
        if titel is None:
            titel = str(nieuw)
        newpage = Page(self.nb, -1, mf=self)
        if note is not None:
            newpage.txt.SetValue(note)
        self.nb.AddPage(newpage, titel)
        self.nb.SetSelection(nieuw)

    def goto_previous(self, event=None):
        "switch to previous page in the notebook"
        self.nb.AdvanceSelection(False)

    def goto_next(self, event=None):
        "switch to next page in the notebook"
        self.nb.AdvanceSelection()

    def closetab(self, event=None, pagetodelete=None):
        """sluit de huidige of aangegeven tab
        """
        if pagetodelete is None:
            pagetodelete = self.current
        aant = self.nb.GetPageCount()
        if aant == 1:
            self.afsl()
            self.Destroy()
        else:
            self.nb.DeletePage(pagetodelete)
            currentpage = self.nb.GetPage(self.current)
            currentpage.txt.SetFocus()

    def revive(self, event=None):
        """herleef het scherm vanuit de systray
        """
        self.Show()
        self.tbi.Destroy()

    def close(self, event=None):
        """Quit the application
        """
        self.afsl()
        self.quitting = True
        self.nb.DeleteAllPages()
        self.Destroy()

    def afsl(self):
        """applicatiedata opslaan voorafgaand aan afsluiten
        """
        self.opts["ActiveTab"] = self.nb.GetSelection()
        self.apodata = {0: self.opts}
        for i in range(self.nb.GetPageCount()):
            page = self.nb.GetPage(i)
            title = self.nb.GetPageText(i)
            text = page.txt.GetValue()
            self.apodata[i + 1] = (title, text)
        self.save_notes(self.apodata)

    def helppage(self, event=None):
        """vertoon de hulp pagina met keyboard shortcuts
        """
        dlg = wx.MessageDialog(self, languages[self.opts["language"]]["info"],
                               'Apropos', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def confirm(self, setting='', textitem=''):
        """Vraag om bevestiging
        """
        if self.opts[setting]:
            with CheckDialog(self, -1, 'Apropos',
                             message=languages[self.opts["language"]][textitem]) as dlg:
                dlg.ShowModal()
                if dlg.check.GetValue():
                    self.opts[setting] = False

    def asktitle(self, event=None):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        dlg = wx.TextEntryDialog(self, languages[self.opts["language"]]["ask_title"],
                                 'Apropos', self.nb.GetPageText(self.current))
        if dlg.ShowModal() == wx.ID_OK:
            self.nb.SetPageText(self.current, dlg.GetValue())
        dlg.Destroy()

    def choose_language(self, event=None):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(x, y["language"]) for x, y in languages.items()]
        dlg = wx.SingleChoiceDialog(
            self, languages[self.opts["language"]]["ask_language"], "Apropos",
            [x[1] for x in data], wx.CHOICEDLG_STYLE)
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["language"]:
                dlg.SetSelection(idx)
                break
        h = dlg.ShowModal()
        if h == wx.ID_OK:
            sel = dlg.GetStringSelection()
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == sel:
                    self.opts["language"] = data[idx][0]
                    break
        dlg.Destroy()

    def options(self, event=None):
        """check settings to show various messages"""
        with OptionsDialog(self, -1) as dlg:
            h = dlg.ShowModal()
            if h == wx.ID_APPLY:
                for keyvalue, control in dlg.controls:
                    self.opts[keyvalue] = control.GetValue()


def main(file, title, log=False):
    """starts the application by calling the MainFrame class
    """
    if log:
        app = wx.App(redirect=True, filename="apropos.log")
    else:
        app = wx.App(redirect=False)
    MainFrame(None, file, title, -1)
    app.MainLoop()
