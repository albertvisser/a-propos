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
        self.apoicon = wx.Icon(iconame, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.apoicon)

    def init_trayicon(self, iconame, tooltip):
        """create an icon to show in the systray

        tooltip argument is for compatibility with qt version
        """
        # tray icon wordt pas opgezet in de hide() methode

    def setup_tabwidget(self, change_page, close_page):
        "build the container to show the tabs in"
        pnl = self  # wx.Panel(self, -1)
        self.nb = wx.Notebook(pnl)
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
            menuitem = wx.MenuItem(None, wx.ID_ANY, label)
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

    def get_current_page(self):  # , event=None):
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
        """get data and setup notebook
        """
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
        "clear out the last remaining tab"
        self.nb.SetPageText(self.master.current, "1")
        self.nb.GetPage(self.master.current).txt.SetValue("")

    def delete_page(self, page_number):
        "delete the chosen tab"
        self.nb.DeletePage(page_number)
        self.set_focus_to_page()

    def hide_app(self):
        """minimize to tray
        """
        self.tray_icon = TaskbarIcon(self, self.apoicon)
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
        """show a message in a box
        """
        with wx.MessageDialog(self, text, 'Apropos', wx.OK | wx.ICON_INFORMATION) as dlg:
            dlg.ShowModal()

    # def show_dialog(self, cls, options):
    def show_dialog(self, dlg):
        """handel custom dialoog af"""
        # parentdlg = cls(self, **options)
        # with parentdlg.gui as dlg:
        with dlg:
            result = dlg.ShowModal()
            # parentdlg.dialog_data = parentdlg.confirm()
            data = dlg.master.confirm()
        # return result == wx.ID_OK, parentdlg.dialogdata
        return result == wx.ID_OK, data

    def get_text(self, prompt, initial=''):
        """handel dialoog om tekst op te geven af
        """
        with wx.TextEntryDialog(self, prompt, 'Apropos', initial) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            text = dlg.GetValue()
        return text, ok

    def set_page_title(self, pageno, title):
        "set (change) a page's title"
        self.nb.SetPageText(pageno, title)

    def get_item(self, prompt, itemlist, initial=None):
        """handel dialoog om tekst te selecteren af
        """
        with wx.SingleChoiceDialog(self, prompt, 'Apropos', itemlist) as dlg:
            if initial is not None:
                dlg.SetSelection(initial)
            ok = dlg.ShowModal() == wx.ID_OK
            # text = dlg.GetValue()
            text = dlg.GetStringSelection()
        return text, ok

    # niet in qt versie geïmplementeerd en ook niet in main.py
    def on_left_doubleclick(self, event):
        """reageert op dubbelklikken op tab t.b.v. verwijderen pagina
        """
        x = event.GetX()
        y = event.GetY()
        item = self.nb.HitTest((x, y))[0]
        self.closetab(item)
        event.Skip()

    # niet geherimplementeerd in Qt, hier wel nodig
    def close(self, event=None):
        """Quit the application
        """
        # self.afsl()  --> naar main
        self.quitting = True
        self.nb.DeleteAllPages()
        self.Destroy()

    def set_screen_dimensions(self, pos, size):
        "vensterpositie instellen zoals aangegeven"
        x, y = (int(x) for x in pos.split('x'))
        w, h = (int(x) for x in size.split('x'))
        self.SetPosition((x, y))
        self.SetSize((w, h))

    def get_screen_dimensions(self):
        "uitgelezen vensterpositie teruggeven"
        pos = self.GetPosition()
        size = self.GetSize()
        # return str(pos), str(size)
        return f'{pos.x}x{pos.y}', f'{size.GetWidth()}x{size.GetHeight()}'


class Page(wx.Panel):
    "Panel subclass voor de notebook pagina's"
    def __init__(self, parent):
        # wx.Panel.__init__(self, parent)
        super().__init__(parent)
        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=DFLT_SIZE)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(self.txt, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer0)
        sizer0.SetSizeHints(self)
        self.Layout()


class CheckDialog(wx.Dialog):
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden

    Eventueel ook te implementeren m.b.v. wx.RichMessageDialog
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        super().__init__(parent, title='Apropos', size=(-1, 120))
        self.SetIcon(parent.apoicon)
        # pnl = wx.Panel(self)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        # pnl.SetSizer(self.vsizer)
        # pnl.SetAutoLayout(True)
        # self.vsizer.Fit(pnl)
        # self.vsizer.SetSizeHints(pnl)
        # pnl.Layout()
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_label(self, labeltext):
        """create a text on the screen
        """
        self.vsizer.Add(wx.StaticText(self, label=labeltext), 1, wx.ALL, 5)

    def add_checkbox(self, caption, value):
        """create a checkbox
        """
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, label=caption)
        check.SetValue(value)
        hsizer.Add(check, 0, wx.EXPAND)
        self.vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return check

    def add_ok_buttonbox(self):
        """create a button strip with handlers
        """
        self.vsizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.ALIGN_CENTER_HORIZONTAL)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.GetValue()


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        super().__init__(parent, title='Apropos')
        # pnl = self  # wx.Panel(self, -1)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.gsizer = wx.FlexGridSizer(cols=2)
        self.vsizer.Add(self.gsizer, 0,
                        wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_checkbox_line_to_grid(self, row, labeltext, value):
        """create a line to turn an option on/off
        """
        # FlexGridsizer heeft row / col niet nodig
        self.gsizer.Add(wx.StaticText(self, label=labeltext), 1, wx.ALL, 5)
        chk = wx.CheckBox(self)
        chk.SetValue(value)
        self.gsizer.Add(chk, 1, wx.ALL, 5)
        return chk

    def add_buttonbox(self, okvalue, cancelvalue):
        """create a button strip with handlers
        """
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, id=wx.ID_OK, label=okvalue)
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        # self.SetAffirmativeId(wx.ID_APPLY)
        btn = wx.Button(self, id=wx.ID_CLOSE, label=cancelvalue)
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        # sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        self.vsizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

    def get_checkbox_value(self, check):
        """return the value of a checkbox
        """
        return check.GetValue()


class TaskbarIcon(wx.adv.TaskBarIcon):
    "icon in the taskbar"

    def __init__(self, parent, icon):
        # super().__init__(wx.adv.TBI_DOCK)
        # wx.adv.TaskBarIcon.__init__(self)
        super().__init__()
        self.id_revive = wx.NewIdRef()
        # self.SetIcon(wx.Icon(iconame, wx.BITMAP_TYPE_ICO), tooltip="Click to revive Apropos")
        self.SetIcon(icon, tooltip="Click to revive Apropos")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, parent.master.revive)
        self.Bind(wx.EVT_MENU, parent.master.revive, id=self.id_revive)

    def CreatePopupMenu(self):
        """reimplemented"""
        menu = wx.Menu()
        menu.Append(self.id_revive, 'Revive Apropos')
        return menu
