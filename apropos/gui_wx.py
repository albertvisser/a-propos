"""apropos/gui_wx.py: presentation layer, wxPython version
"""
import wx
import wx.adv
# import apropos.shared as shared
# languages = shared.languages
DFLT_SIZE = (650, 400)


class AproposGui(wx.Frame):
    """main class voor de applicatie
    """
    def __init__(self, master, parent=None, fname='', title='Apropos'):
        self.app = wx.App()
        self.master = master
        # self.parent = parent
        self.quitting = False
        # wx.Frame.__init__(self, parent, title=title, pos=(10, 10))  # , size=DFLT_SIZE)
        super().__init__(parent, title=title, pos=(10, 10))  # , size=DFLT_SIZE)
        self.Bind(wx.EVT_CLOSE, self.close)

    def set_appicon(self, iconame):
        "give the window an icon"
        self.SetIcon(wx.Icon(iconame, wx.BITMAP_TYPE_ICO))

    def init_trayicon(self, iconame, tooltip):
        "create an icon to show in the systray"
        self.tray_icon = TaskbarIcon(self, iconame)

    def setup_tabwidget(self, change_page, close_page):
        "build the container to show the tabs in"
        pnl = self  # wx.Panel(self, -1)
        self.nb = wx.Notebook(pnl, -1)
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, change_page)  # self.page_changed)
        self.nb.Bind(wx.EVT_LEFT_DCLICK, close_page)   # self.on_left_doubleclick)
        self.nb.Bind(wx.EVT_MIDDLE_DOWN, close_page)   # self.on_left_doubleclick)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.nb, 1, wx.EXPAND)  # | wx.ALL, 10)
        pnl.SetSizer(sizer0)
        sizer0.SetSizeHints(pnl)

    def setup_shortcuts(self, handler_dict):
        "create the app navigation"
        accel_list = []
        for label, data in handler_dict.items():
            shortcuts, handler = data
            menuitem = wx.MenuItem(None, -1, label)
            self.Bind(wx.EVT_MENU, handler, menuitem)
            for key in shortcuts:
                accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
                ok = accel.FromString(key)
                if ok:
                    accel_list.append(accel)
        accel_table = wx.AcceleratorTable(accel_list)
        self.SetAcceleratorTable(accel_table)

    def go(self):
        "show the screen and start the event loop"
        self.Show()
        self.app.MainLoop()

    def get_page_count(self):
        "return number of pages"
        return self.nb.GetPageCount()

    def get_current_page(self):  #  , event=None):
        "return selected page"
        # if event:
        #     return event.GetSelection()  # after changing tab
        return self.nb.GetSelection()

    def set_previous_page(self):
        "switch to previous page in the notebook"
        self.nb.AdvanceSelection(False)

    def set_next_page(self):
        "switch to next page in the notebook"
        self.nb.AdvanceSelection()

    def set_current_page(self, page_number):
        "set selected page"
        self.nb.SetSelection(page_number)
        # conform de oorspronkelijke code zou dit zijn    self.nb.ChangeSelection(page_number)

    def set_focus_to_page(self, event=None):
        "activate (bring to front) selected page"
        # currentpage = self.nb.GetPage(self.get_current_page())
        currentpage = self.nb.GetPage(self.master.current)
        if currentpage:
            currentpage.txt.SetFocus()
        if event:
            event.Skip()

    def clear_all(self):
        self.quitting = True  # bypass page_changed handling
        self.nb.DeleteAllPages()
        self.quitting = not self.quitting

    def new_page(self, nieuw, titel, note):
        """initialiseer een nieuwe tab
        """
        newpage = Page(self.nb)
        if note is not None:
            newpage.txt.SetValue(note)
        self.nb.AddPage(newpage, titel)
        self.nb.SetSelection(nieuw - 1)

    def clear_last_page(self):
        self.nb.SetPageText(self.master.current, "1")
        self.nb.GetPage(self.master.current).txt.SetValue("")

    def delete_page(self, page_number):
        self.nb.DeletePage(page_number)
        self.set_focus_to_page()

    def hide_app(self):
        """minimize to tray
        """
        self.Hide()

    def reshow_app(self, event=None):
        """herleef het scherm vanuit de systray
        """
        self.Show()
        self.tray_icon.Destroy()

    def get_page_title(self, pageno):
        "paginaheader (naam in tab) ophalen"
        return self.nb.GetPageText(pageno)

    def get_page_text(self, pageno):
        "pagina tekst ophalen"
        return self.nb.GetPage(pageno).txt.GetValue()

    def meld(self, text):
        with wx.MessageDialog(self, text, 'Apropos', wx.OK | wx.ICON_INFORMATION) as dlg:
            dlg.ShowModal()

    def show_dialog(self, cls, options):
        """handel custom dialoog af"""
        with cls(self, **options) as dlg:
            if dlg.showmodal() == wx.ID_OK:
                dlg.accept()

    def get_text(self, prompt, initial=''):
        """handel dialoog om tekst op te geven af
        """
        with wx.TextEntryDialog(self, prompt, 'Apropos', initial) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            text = dlg.GetValue()
        return text, ok

    def set_page_title(self, pageno, title):
        self.nb.SetPageText(pageno, title)

    def get_item(self, prompt, itemlist, initial=None):
        """handel dialoog om tekst te selecteren af
        """
        with wx.SingleChoiceDialog(self, prompt, 'Apropos', itemlist) as dlg:
            if initial is not None:
                dlg.SetSelection(initial)
            ok = dlg.ShowModal() == wx.ID_OK
            text = dlg.GetValue()
        return text, ok

    # niet in qt versie is geïmplementeerd en ook niet in main.py
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

    # niet geherimplementeerd in Qt, wel nodig
    def close(self, event=None):
        """Quit the application
        """
        # self.afsl()  --> naar main
        self.quitting = True
        self.nb.DeleteAllPages()
        self.Destroy()


class Page(wx.Panel):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.txt = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=DFLT_SIZE)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.txt, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer0)
        sizer0.SetSizeHints(self)
        self.Layout()


class CheckDialog(wx.Dialog):
    """Dialog die kan worden ingesteld om iets niet nogmaals te tonen

    wordt aangestuurd met de boodschap die in de dialoog moet worden getoond
    """
    def __init__(self, parent, title, message="", option="", caption=True):

        self.parent = parent
        wx.Dialog.__init__(self, parent, title=title, pos=wx.DefaultPosition, size=(-1, 120),
                           style=wx.DEFAULT_DIALOG_STYLE)
        pnl = self  # wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl, -1, message), 1, wx.ALL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.check = wx.CheckBox(pnl, -1, caption)
        self.check.SetValue(self.parent.master.opts[option])
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

    def accept(self):
        "(un)set the setting"
        self.parent.master.opts[self.option] = not self.check.GetValue()


class TaskbarIcon(wx.adv.TaskBarIcon):
    "icon in the taskbar"
    id_revive = wx.NewIdRef()

    def __init__(self, parent, iconame):
        # super().__init__(wx.adv.TBI_DOCK)
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(iconame, wx.BITMAP_TYPE_ICO), tooltip="Click to revive Apropos")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, parent.master.revive)
        self.Bind(wx.EVT_MENU, parent.master.revive, id=self.id_revive)

    def CreatePopupMenu(self):
        """reimplemented"""
        menu = wx.Menu()
        menu.Append(self.id_revive, 'Revive Apropos')
        return menu


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent, title, sett2text=None):
        self.parent = parent
        if sett2text is None:
            sett2text = {}
        super().__init__(parent, title='A Propos Settings')
        pnl = self  # wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.FlexGridSizer(cols=2)
        self.controls = []
        for key, value in self.parent.opts.items():
            if key not in sett2text:
                continue
            sizer1.Add(wx.StaticText(pnl, -1, sett2text[key]), 1, wx.ALL, 5)
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

    def accept(self):
        "(un)set the aettings"
        for keyvalue, control in self.controls:
            self.parent.opts[keyvalue] = control.isChecked()
