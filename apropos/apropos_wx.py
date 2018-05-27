# -*- coding: utf-8 -*-
"""apropos_wx.py

presentation layer and most of the application logic, wxPython (2) version
"""
from __future__ import print_function
import pathlib  # os
## import sys
import wx
from .apomixin import ApoMixin, languages
HERE = pathlib.Path(__file__).parent  # os.path.dirname(__file__)


class Page(wx.Panel):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent, id, mf):
        wx.Panel.__init__(self, parent, id)
        self.txt = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.txt.Bind(wx.EVT_KEY_DOWN, mf.on_key)
        ## self.Bind(wx.EVT_TEXT, self.OnEvtText, self.txt)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.txt, 1, wx.EXPAND)
        sizer0.Add(sizer1, 1, wx.EXPAND)
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
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
        pnl = wx.Panel(self, -1)
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
        sizer0.Add(sizer1, 0,
                   wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
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
        wx.Frame.__init__(self, parent, id, title=title, pos=(10, 10),
                          size=(650, 400))
        self.Bind(wx.EVT_CLOSE, self.afsl)
        self.apoicon = wx.Icon(str(HERE / "apropos.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.apoicon)
        pnl = wx.Panel(self, -1)
        self.nb = wx.Notebook(pnl, -1)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.page_changed)
        self.nb.Bind(wx.EVT_LEFT_DCLICK, self.on_left_doubleclick)
        self.nb.Bind(wx.EVT_MIDDLE_DOWN, self.on_left_doubleclick)
        self.nb.Bind(wx.EVT_LEFT_UP, self.on_left_release)
        self.nb.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.set_apofile(fname)
        self.initapp()
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.nb, 1, wx.EXPAND)
        sizer0.Add(sizer1, 1, wx.EXPAND)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()
        self.Bind(wx.EVT_CLOSE, self.afsl)
        self.Show()

    def page_changed(self, event=None):
        """pagina aanpassen nadat een andere gekozen is
        """
        self.current = event.GetSelection()
        currentpage = self.nb.GetPage(self.current)
        currentpage.txt.SetFocus()
        ## if sys.platform == 'win32':
        if True:  # os.name == 'nt':
            event.Skip()

    def on_left_release(self, evt=None):
        """reageert op muis loslaten na selecteren andere tab
        """
        currentpage = self.nb.GetPage(self.current)
        currentpage.txt.SetFocus()
        evt.Skip()

    def on_key(self, event=None):
        """afhandeling toetsaanslagen / toetsencombinaties
        """
        skip = True
        keycode = event.GetKeyCode()
        if event.GetModifiers() == wx.MOD_CONTROL:  # evt.ControlDown()
            if keycode == ord("R"):    # 76: Ctrl-R reload tabs
                self.load_data()
            elif keycode == ord("N"):  # 78: Ctrl-N nieuwe tab
                self.newtab()
            elif keycode == ord("W"):  # 87: Ctrl-W tab sluiten
                self.closetab()
                skip = False
            ## elif keycode == wx.WXK_LEFT or keycode == wx.WXK_NUMPAD_LEFT: #  keycode == 314
            ##     self.nb.AdvanceSelection(False)
            ## elif keycode == wx.WXK_RIGHT or keycode == wx.WXK_NUMPAD_RIGHT: #  keycode == 316
            ##     self.nb.AdvanceSelection()
            elif keycode == ord("H"):  # 72: Ctrl-H Hide/minimize
                self.hide_app()
            elif keycode == ord("S"):  # 83: Ctrl-S saven zonder afsluiten
                self.save_data()
            elif keycode == ord("Q"):  # 81: Ctrl-Q afsluiten na saven
                self.afsl()
                self.Destroy()
            elif keycode == ord("L"):  # Ctrl-L choose Language
                self.choose_language()
        elif keycode == wx.WXK_F1:
            self.helppage()
        elif keycode == wx.WXK_F2:
            self.asktitle()
        elif keycode == wx.WXK_ESCAPE:
            self.afsl()
            self.Destroy()
        if event and skip:
            event.Skip()

    def on_left_doubleclick(self, event=None):
        """reageert op dubbelklikken op tab t.b.v. verwijderen pagina
        """
        x = event.GetX()
        y = event.GetY()
        item, _ = self.nb.HitTest((x, y))
        self.closetab(item)
        event.Skip()

    def load_data(self):
        """get data and setup notebook
        """
        self.nb.DeleteAllPages()
        self.initapp()
        self.confirm(setting="NotifyOnLoad", textitem="load_text")

    def hide_app(self):
        """minimize to tray
        """
        self.confirm(setting="AskBeforeHide", textitem="hide_text")
        self.tbi = wx.TaskBarIcon()
        self.tbi.SetIcon(self.apoicon, "Click to revive Apropos")
        wx.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
        self.Hide()

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
            self.nb.ChangeSelection(self.opts["ActiveTab"])
            self.current = self.opts["ActiveTab"]
        else:
            self.newtab()
            self.current = 0

    def newtab(self, titel=None, note=None):
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

    def closetab(self, pagetodelete=None):
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

    def revive(self, event=None):
        """herleef het scherm vanuit de systray
        """
        self.Show()
        self.tbi.Destroy()

    def afsl(self, event=None):
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
        if event:
            event.Skip()

    def helppage(self):
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
            dlg = CheckDialog(self, -1, 'Apropos',
                              message=languages[self.opts["language"]][textitem])
            dlg.ShowModal()
            if dlg.check.GetValue():
                self.opts[setting] = False
            dlg.Destroy()

    def asktitle(self):
        """toon dialoog om tab titel in te vullen/aan te passen en verwerk antwoord
        """
        dlg = wx.TextEntryDialog(self, languages[self.opts["language"]]["ask_title"],
                                 'Apropos', self.nb.GetPageText(self.current))
        if dlg.ShowModal() == wx.ID_OK:
            self.nb.SetPageText(self.current, dlg.GetValue())
        dlg.Destroy()

    def choose_language(self):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(x, y["language"]) for x, y in languages.iteritems()]
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


def main(fname, title, log=False):
    """starts the application by calling the MainFrame class
    """
    print(fname)
    if log:
        print('with logging')
        app = wx.App(redirect=True, filename="apropos.log")
    else:
        print('no logging')
        app = wx.App(redirect=False)
    MainFrame(None, fname, title, -1)
    app.MainLoop()
