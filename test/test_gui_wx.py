"""unittests for ./apropos/gui_wx.py
"""
import types
from mockgui import mockwxwidgets as mockwx
from apropos import gui_wx as testee

def setup_mainwindow(monkeypatch, capsys):
    """stub for setting up MainWindow object
    """
    monkeypatch.setattr(testee.wx, 'Frame', mockwx.MockFrame)
    monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
    testobj = testee.MainWindow(MockApropos())
    assert capsys.readouterr().out == ('called NoteTree.__init__\n'
                                       'called app.__init__\n')
    return testobj


class MockApropos:
    """testdouble for Apropos object
    """
    def __init__(self):
        print("called Apropos.__init__")


class TestAproposGui:
    """unittest for gui_wx.AproposGui
    """

    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.AproposGself, ui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AproposGui.__init__ with args', args)
        monkeypatch.setattr(testee.AproposGui, '__init__', mock_init)
        master = MockApropos()
        testobj = testee.AproposGui(master)
        assert capsys.readouterr().out == ('called Apropos.__init__\n'
                                           f'called AproposGui.__init__ with args ({master},)\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AproposGui.__init__
        """
        # monkeypatch.setattr(testee.wx, 'Frame', mockwx.MockFrame)
        monkeypatch.setattr(testee.wx.Frame, '__init__', mockwx.MockFrame.__init__)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        # monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
        monkeypatch.setattr(testee.wx.App, '__init__', mockwx.MockApp.__init__)
        testmaster = MockApropos()
        assert capsys.readouterr().out == 'called Apropos.__init__\n'
        testobj = testee.AproposGui(testmaster, parent=None)  # , fname='', title='Apropos')
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called frame.__init__ with args (None,) {'title': 'Apropos', 'pos': (10, 10)}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_CLOSE}, {testobj.close})\n")

    def test_set_appicon(self, monkeypatch, capsys):
        """unittest for AproposGui.set_appicon
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetIcon', mockwx.MockFrame.SetIcon)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        # assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        testobj.set_appicon('iconame')
        assert capsys.readouterr().out == (
                f"called Icon.__init__ with args ('iconame', {testee.wx.BITMAP_TYPE_ICO})\n"
                "called Frame.SetIcon with args (Icon created from 'iconame',)\n")

    def test_init_trayicon(self, monkeypatch, capsys):
        """unittest for AproposGui.init_trayicon
        """
        # deliberately left empty

    def test_setup_tabwidget(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_tabwidget
        """
        monkeypatch.setattr(testee.wx, 'Notebook', mockwx.MockNoteBook)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Frame, 'SetSizer', mockwx.MockFrame.SetSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setup_tabwidget('change_page_callback', 'close_page_callback')
        assert capsys.readouterr().out == (
                f"called NoteBook.__init__ with args ({testobj},)\n"
                "called NoteBook.Bind with args"
                f" ({testee.wx.EVT_NOTEBOOK_PAGE_CHANGED}, 'change_page_callback')\n"
                "called NoteBook.Bind with args"
                f" ({testee.wx.EVT_LEFT_DCLICK}, 'close_page_callback')\n"
                "called NoteBook.Bind with args"
                f" ({testee.wx.EVT_MIDDLE_DOWN}, 'close_page_callback')\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                f"called vert sizer.Add with args <item> (1, {testee.wx.EXPAND})\n"
                "called Frame.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n")

    def test_setup_shortcuts(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_shortcuts
        """
        def callback(*args):
            "dummy function"
        def mock_repr(self):
            return 'new menuitem'
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(mockwx.MockMenuItem, '__repr__', mock_repr)
        monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        monkeypatch.setattr(testee.wx.Frame, 'SetAcceleratorTable',
                            mockwx.MockFrame.SetAcceleratorTable)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mockwx.MockFrame.Bind)
        handler_dict = {}
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setup_shortcuts(handler_dict)
        assert capsys.readouterr().out == (
                "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
                "called Frame.SetAcceleratorTable\n")
        handler_dict = {'one': (['xx', 'yy'], callback), 'Two': ('', None)}
        testobj.setup_shortcuts(handler_dict)
        assert capsys.readouterr().out == (
                "called MenuItem.__init__ with args (None, -1, 'one') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, {callback})\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('xx',)\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('yy',)\n"
                "called MenuItem.__init__ with args (None, -1, 'Two') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, None)\n"
                "called AcceleratorTable.__init__ with 2 AcceleratorEntries\n"
                "called Frame.SetAcceleratorTable\n")
        monkeypatch.setattr(mockwx.MockAcceleratorEntry, 'FromString', lambda *x: False)
        testobj.setup_shortcuts(handler_dict)
        assert capsys.readouterr().out == (
                "called MenuItem.__init__ with args (None, -1, 'one') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, {callback})\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called MenuItem.__init__ with args (None, -1, 'Two') {}\n"
                f"called Frame.Bind with args ({testee.wx.EVT_MENU}, None)\n"
                "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
                "called Frame.SetAcceleratorTable\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for AproposGui.go
        """
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockwx.MockApp()
        assert capsys.readouterr().out == "called app.__init__ with args ()\n"
        testobj.go()
        assert capsys.readouterr().out == ("called frame.Show\n"
                                           "called app.MainLoop\n")

    def test_get_page_count(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_count
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        assert testobj.get_page_count() == "pagecount"
        assert capsys.readouterr().out == "called NoteBook.GetPageCount with args ()\n"

    def test_get_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.get_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        assert testobj.get_current_page() == "selection"
        assert capsys.readouterr().out == "called NoteBook.GetSelection with args ()\n"

    def test_set_previous_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_previous_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.set_previous_page()
        assert capsys.readouterr().out == "called NoteBook.AdvanceSelection with args (False,)\n"

    def test_set_next_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_next_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.set_next_page()
        assert capsys.readouterr().out == "called NoteBook.AdvanceSelection with args ()\n"

    def test_set_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.set_current_page('page_number')
        assert capsys.readouterr().out == "called NoteBook.SetSelection with args ('page_number',)\n"

    def test_set_focus_to_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_focus_to_page
        """
        def mock_get(self, *args):
            print('called NoteBook.GetPage with args', args)
            return types.SimpleNamespace(txt=mockwx.MockEditor())
        def mock_get_2(self, *args):
            print('called NoteBook.GetPage with args', args)
            return None
        monkeypatch.setattr(mockwx.MockNoteBook, 'GetPage', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.master = types.SimpleNamespace(current='current page')
        testobj.set_focus_to_page(event=None)
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args ('current page',)\n"
                                           "called Editor.__init__ with args ()\n"
                                           "called editor.SetFocus\n")
        testobj.master = types.SimpleNamespace(current='')
        monkeypatch.setattr(mockwx.MockNoteBook, 'GetPage', mock_get_2)
        e = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj.set_focus_to_page(event=e)
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args ('',)\n"
                                           "called event.Skip\n")

    def test_clear_all(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.clear_all()
        assert not testobj.quitting
        assert capsys.readouterr().out == "called NoteBook.DeleteAllPages with args ()\n"

    def test_new_page(self, monkeypatch, capsys):
        """unittest for AproposGui.new_page
        """
        class MockPage:
            "stub"
            def __init__(self, *args):
                print('called Page.__init__ with args', args)
                self.txt = mockwx.MockEditor()
            def __repr__(self):
                return "'new page'"
        monkeypatch.setattr(testee, 'Page', MockPage)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.new_page(2, 'titel', 'note')
        assert capsys.readouterr().out == (
                f"called Page.__init__ with args ({testobj.nb},)\n"
                "called Editor.__init__ with args ()\n"
                "called editor.SetValue with arg `note`\n"
                "called NoteBook.AddPage with args ('new page', 'titel')\n"
                "called NoteBook.SetSelection with args (1,)\n")
        testobj.new_page(2, 'titel', None)
        assert capsys.readouterr().out == (
                f"called Page.__init__ with args ({testobj.nb},)\n"
                "called Editor.__init__ with args ()\n"
                "called NoteBook.AddPage with args ('new page', 'titel')\n"
                "called NoteBook.SetSelection with args (1,)\n")

    def test_clear_last_page(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_last_page
        """
        def mock_get(self, *args):
            print('called NoteBook.GetPage with args', args)
            return types.SimpleNamespace(txt=mockwx.MockEditor())
        monkeypatch.setattr(mockwx.MockNoteBook, 'GetPage', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        testobj.master = types.SimpleNamespace(current='current page')
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.clear_last_page()
        assert capsys.readouterr().out == (
                "called NoteBook.SetPageText with args ('current page', '1')\n"
                "called NoteBook.GetPage with args ('current page',)\n"
                "called Editor.__init__ with args ()\n"
                "called editor.SetValue with arg ``\n")

    def test_delete_page(self, monkeypatch, capsys):
        """unittest for AproposGui.delete_page
        """
        def mock_get(self, *args):
            print('called NoteBook.GetPage with args', args)
            return types.SimpleNamespace(txt=mockwx.MockEditor())
        monkeypatch.setattr(mockwx.MockNoteBook, 'GetPage', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        testobj.master = types.SimpleNamespace(current='current page')
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.delete_page('page_number')
        assert capsys.readouterr().out == (
                "called NoteBook.DeletePage with args ('page_number',)\n"
                "called NoteBook.GetPage with args ('current page',)\n"
                "called Editor.__init__ with args ()\n"
                "called editor.SetFocus\n")

    def test_hide_app(self, monkeypatch, capsys):
        """unittest for AproposGui.hide_app
        """
        def mock_init(self, *args):
            print('called TaskbarIcon.__init__ with args', args)
        monkeypatch.setattr(testee.TaskbarIcon, '__init__', mock_init)
        monkeypatch.setattr(testee.wx.Frame, 'Hide', mockwx.MockFrame.Hide)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.apoicon = 'apoicon'
        testobj.hide_app()
        assert capsys.readouterr().out == (
                f"called TaskbarIcon.__init__ with args ({testobj}, 'apoicon')\n"
                "called frame.Hide\n")

    def test_reshow_app(self, monkeypatch, capsys):
        """unittest for AproposGui.reshow_app
        """
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tray_icon = mockwx.MockTrayIcon()
        assert capsys.readouterr().out == "called TrayIcon.__init__ with args ()\n"
        testobj.reshow_app()
        assert capsys.readouterr().out == ("called frame.Show\n"
                                           "called trayicon.Destroy\n")

    def test_get_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        assert testobj.get_page_title('pageno') == "title"
        assert capsys.readouterr().out == "called NoteBook.GetPageText with args ('pageno',)\n"

    def test_get_page_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_text
        """
        def mock_get(self, *args):
            print('called NoteBook.GetPage with args', args)
            return types.SimpleNamespace(txt=mockwx.MockEditor())
        monkeypatch.setattr(mockwx.MockNoteBook, 'GetPage', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        assert testobj.get_page_text('pageno') == "fake editor value"
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args ('pageno',)\n"
                                           "called Editor.__init__ with args ()\n"
                                           "called editor.GetValue\n")

    def test_meld(self, monkeypatch, capsys):
        """unittest for AproposGui.meld == "expected_result"
        """
        monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.meld('text')
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, "
                f"'text', 'Apropos', {testee.wx.OK | testee.wx.ICON_INFORMATION}) {{}}\n"
                "called MessageDialog.ShowModal\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for AproposGui.show_dialog
        """
        def mock_confirm():
            print('called dialogparent.confirm')
            return 'data'
        def mock_show(self):
            print('called dialog.ShowModal')
            return testee.wx.ID_CANCEL
        def mock_show_2(self):
            print('called dialog.ShowModal')
            return testee.wx.ID_OK
        monkeypatch.setattr(mockwx.MockDialog, 'ShowModal', mock_show)
        dlg = mockwx.MockDialog('parent')
        # assert capsys.readouterr().out == f"called Dialog.__init__ with args {parent} () {{}}\n"
        assert capsys.readouterr().out == "called Dialog.__init__ with args () {}\n"
        dlg.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_dialog(dlg) == (False, 'data')
        assert capsys.readouterr().out == ("called dialog.ShowModal\n"
                                           "called dialogparent.confirm\n")
        monkeypatch.setattr(mockwx.MockDialog, 'ShowModal', mock_show_2)
        assert testobj.show_dialog(dlg) == (True, 'data')
        assert capsys.readouterr().out == ("called dialog.ShowModal\n"
                                           "called dialogparent.confirm\n")

    def test_get_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_text
        """
        monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_text('prompt')
        assert capsys.readouterr().out == (
                "called TextDialog.__init__ with args ('prompt', 'Apropos', '') {}\n"
                "called TextDialog.ShowModal\n"
                "called TextDialog.GetValue\n")
        testobj.get_text('prompt', 'initial')
        assert capsys.readouterr().out == (
                "called TextDialog.__init__ with args ('prompt', 'Apropos', 'initial') {}\n"
                "called TextDialog.ShowModal\n"
                "called TextDialog.GetValue\n")

    def test_set_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.set_page_title('pageno', 'title')
        assert capsys.readouterr().out == (
                "called NoteBook.SetPageText with args ('pageno', 'title')\n")

    def test_get_item(self, monkeypatch, capsys):
        """unittest for AproposGui.get_item
        """
        def mock_show(self):
            return 'canceled'
        monkeypatch.setattr(testee.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item('prompt', ['item', 'list']) == ('selected value', True)
        assert capsys.readouterr().out == (
                "called ChoiceDialog.__init__ with args ('prompt', 'Apropos')\n"
                "called ChoiceDialog.ShowModal\n"
                "called ChoiceDialog.GetStringSelection\n")
        monkeypatch.setattr(mockwx.MockChoiceDialog, 'ShowModal', mock_show)
        assert testobj.get_item('prompt', ['xx', 'yy'], 'xx') == ('selected value', False)
        assert capsys.readouterr().out == (
                "called ChoiceDialog.__init__ with args ('prompt', 'Apropos')\n"
                # "called ChoiceDialog.ShowModal\n"
                "called ChoiceDialog.SetSelection with arg 'xx'\n"
                "called ChoiceDialog.GetStringSelection\n")

    def test_on_left_doubleclick(self, monkeypatch, capsys):
        """unittest for AproposGui.on_left_doubleclick
        """
        def mock_closetab(*args):
            print('called MainGui.closetab with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        testobj.closetab = mock_closetab
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == ("called NoteBook.__init__ with args ()\n"
                                           "called event.__init__ with args ()\n")
        testobj.on_left_doubleclick(event)
        assert capsys.readouterr().out == ("called event.GetX\n"
                                           "called event.GetY\n"
                                           "called NoteBook.HitTest with args (('x', 'y'),)\n"
                                           "called MainGui.closetab with args ('itemno',)\n"
                                           "called event.Skip\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for AproposGui.close
        """
        monkeypatch.setattr(testee.wx.Frame, 'Destroy', mockwx.MockFrame.Destroy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.close()
        assert testobj.quitting
        assert capsys.readouterr().out == ("called NoteBook.DeleteAllPages with args ()\n"
                                           "called Frame.Destroy with args ()\n")

    def test_set_screen_dimensions(self, monkeypatch, capsys):
        """unittest for AproposGui.set_screen_dimensions
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetPosition', mockwx.MockFrame.SetPosition)
        monkeypatch.setattr(testee.wx.Frame, 'SetSize', mockwx.MockFrame.SetSize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_screen_dimensions('11x12', '200x100')
        assert capsys.readouterr().out == ("called Frame.SetPosition with args ((11, 12),)\n"
                                           "called Frame.SetSize with args ((200, 100),)\n")

    def test_get_screen_dimensions(self, monkeypatch, capsys):
        """unittest for AproposGui.get_screen_dimensions
        """
        monkeypatch.setattr(testee.wx.Frame, 'GetPosition', mockwx.MockFrame.GetPosition)
        monkeypatch.setattr(testee.wx.Frame, 'GetSize', mockwx.MockFrame.GetSize)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_screen_dimensions() == ('1x2', '100x10')
        assert capsys.readouterr().out == ("called Frame.GetPosition\n"
                                           "called Point.__init__ with args (1, 2)\n"
                                           "called Frame.GetSize\n"
                                           "called Size.__init__ with args (100, 10)\n"
                                           "called Size.GetWidth\n"
                                           "called Size.GetHeight\n")


class TestPage:
    """unittest for gui_wx.Page
    """

    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Page object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page.__init__ with args', args)
        monkeypatch.setattr(testee.Page, '__init__', mock_init)
        testobj = testee.Page()
        assert capsys.readouterr().out == 'called Page.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Page.__init__
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Panel, '__init__', mockwx.MockPanel.__init__)
        monkeypatch.setattr(testee.wx.Panel, 'Layout', mockwx.MockPanel.Layout)
        monkeypatch.setattr(testee.wx.Panel, 'SetSizer', mockwx.MockPanel.SetSizer)
        parent = testee.wx.Panel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        testobj = testee.Page(parent)
        assert isinstance(testobj.txt, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called Panel.__init__ with args ({parent},) {{}}\n"
                f"called TextCtrl.__init__ with args ({testobj},)"
                f" {{'style': {testee.wx.TE_MULTILINE}, 'size': {testee.DFLT_SIZE}}}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.Add with args"
                f" <item> (1, {testee.wx.EXPAND | testee.wx.ALL}, 10)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called Panel.Layout with args ()\n")


class TestCheckDialog:
    """unittest for gui_wx.CheckDialog
    """
    # def setup_testobj(self, monkeypatch, capsys):
    #     """stub for gui_wx.CheckDialog object

    #     create the object skipping the normal initialization
    #     intercept messages during creation
    #     return the object so that methods can be monkeypatched in the caller
    #     """
    #     def mock_init(self, *args):
    #         """stub
    #         """
    #         print('called CheckDialog.__init__ with args', args)
    #     monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
    #     testobj = testee.CheckDialog()
    #     assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()\n'
    #     return testobj

    # def test_init(self, monkeypatch, capsys):
    #     """unittest for CheckDialog.__init__
    #     """
    #     monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
    #     monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
    #     monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
    #     monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
    #     monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
    #     monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
    #     monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
    #     monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
    #     parent = types.SimpleNamespace(master=types.SimpleNamespace(opts={'xxx': 'yyy'}))
    #     with pytest.raises(KeyError):
    #         testobj = testee.CheckDialog(parent, 'a title',)
    #     capsys.readouterr()    # discard captured print output
    #     testobj = testee.CheckDialog(parent, 'a title', 'a message', 'xxx', 'a caption')
    #     assert testobj.parent == parent
    #     assert isinstance(testobj.check, testee.wx.CheckBox)
    #     assert capsys.readouterr().out == (
    #         "called Dialog.__init__ with args () {'title': 'a title', 'size': (-1, 120)}\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
    #         f"called StaticText.__init__ with args ({testobj},) {{'label': 'a message'}}\n"
    #         f"called vert sizer.Add with args <item> (1, {testee.wx.ALL}, 5)\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
    #         f"called CheckBox.__init__ with args ({testobj},) {{'label': 'a caption'}}\n"
    #         "called checkbox.SetValue with args ('yyy',)\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND})\n"
    #         f"called vert sizer.Add with args <item> (0, {testee.wx.ALIGN_CENTER_HORIZONTAL})\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_OK}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL| testee.wx.ALIGN_CENTER_VERTICAL},"
    #         " 5)\n"
    #         "called dialog.SetSizer with args (vert sizer,)\n"
    #         "called dialog.SetAutoLayout with args (True,)\n"
    #         f"called vert sizer.Fit with args ({testobj},)\n"
    #         f"called vert sizer.SetSizeHints with args ({testobj},)\n"
    #         "called dialog.Layout with args ()\n")

    # def test_accept(self, monkeypatch, capsys):
    #     """unittest for CheckDialog.accept
    #     """
    #     def mock_get():
    #         print('called CheckBox.GetValue')
    #         return 'zzz'
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.check = mockwx.MockCheckBox()
    #     assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
    #     testobj.check.GetValue = mock_get
    #     testobj.parent = types.SimpleNamespace(master=types.SimpleNamespace(opts={'xxx': 'yyy'}))
    #     testobj.option = 'xxx'
    #     testobj.accept()
    #     assert capsys.readouterr().out == "called CheckBox.GetValue\n"
    def test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.init
        """
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)

        parent = types.SimpleNamespace(apoicon='icon')
        testobj = testee.CheckDialog('master', parent)
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'Apropos', 'size': (-1, 120)}\n"
                "called Dialog.SetIcon with args ('icon',)\n"
                f'called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n'
                'called dialog.SetSizer with args (vert sizer,)\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                'called dialog.Layout with args ()\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for CheckDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
        testobj = testee.CheckDialog()
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        testobj.add_label('message')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                'called vert sizer.Add with args <item> (1, 240, 5)\n')

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        testobj.add_checkbox('text', 'value')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                f'called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called checkbox.SetValue with args ('value',)\n"
                'called hori sizer.Add with args <item> (0, 8192)\n'
                'called vert sizer.Add with args <item> (0, 256)\n')

    def test_add_ok_buttonbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_ok_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        testobj.add_ok_buttonbox()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                'called dialog.CreateButtonSizer with args (4,)\n'
                'called vert sizer.Add with args <item> (0, 256)\n')

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for OptionsDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        check.SetValue(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")


class TestTaskbarIcon:
    """unittest for gui_wx.TaskbarIcon
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.TaskbarIcon object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TaskbarIcon.__init__ with args', args)
        monkeypatch.setattr(testee.TaskbarIcon, '__init__', mock_init)
        testobj = testee.TaskbarIcon()
        assert capsys.readouterr().out == 'called TaskbarIcon.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.__init__
        """
        def mock_idref():
            "stub"
            print('called wx.NewIdRef')
            return 'xxx'
        def callback(*args):
            "dummy callback, we only need the reference to it"
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, '__init__', mockwx.MockTrayIcon.__init__)
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, 'SetIcon', mockwx.MockTrayIcon.SetIcon)
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, 'Bind', mockwx.MockTrayIcon.Bind)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx, 'NewIdRef', mock_idref)
        parent = types.SimpleNamespace(master=types.SimpleNamespace(revive=callback))
        testobj = testee.TaskbarIcon(parent, 'apoicon')
        assert testobj.id_revive == 'xxx'
        assert capsys.readouterr().out == (
            "called TrayIcon.__init__ with args ()\n"
            "called wx.NewIdRef\n"
            "called trayicon.SetIcon with args ('apoicon',) {'tooltip': 'Click to revive Apropos'}\n"
            "called trayicon.Bind with args"
            f" ({testee.wx.adv.EVT_TASKBAR_LEFT_DCLICK}, {callback}) {{}}\n"
            f"called trayicon.Bind with args ({testee.wx.EVT_MENU}, {callback}) {{'id': 'xxx'}}\n")

    def test_CreatePopupMenu(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.CreatePopupMenu
        """
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.id_revive = 'xxx'
        result = testobj.CreatePopupMenu()
        assert isinstance(result, testee.wx.Menu)
        assert capsys.readouterr().out == (
                "called Menu.__init__ with args ()\n"
                "called menu.Append with args ('xxx', 'Revive Apropos')\n")


class TestOptionsDialog:
    """unittest for gui_wx.OptionsDialog
    """
    # def setup_testobj(self, monkeypatch, capsys):
    #     """stub for gui_wx.OptionsDialog object

    #     create the object skipping the normal initialization
    #     intercept messages during creation
    #     return the object so that methods can be monkeypatched in the caller
    #     """
    #     def mock_init(self, *args):
    #         """stub
    #         """
    #         print('called OptionsDialog.__init__ with args', args)
    #     monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
    #     testobj = testee.OptionsDialog()
    #     assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()\n'
    #     return testobj

    # def test_init(self, monkeypatch, capsys):
    #     """unittest for OptionsDialog.__init__
    #     """
    #     monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
    #     monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockFlexGridSizer)
    #     monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
    #     monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
    #     monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
    #     monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
    #     monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId', mockwx.MockDialog.SetAffirmativeId)
    #     monkeypatch.setattr(testee.wx.Dialog, 'SetEscapeId', mockwx.MockDialog.SetEscapeId)
    #     monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
    #     monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
    #     monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
    #     parent = types.SimpleNamespace(opts={})
    #     testobj = testee.OptionsDialog(parent, 'title')
    #     assert testobj.controls == []
    #     assert capsys.readouterr().out == (
    #         "called Dialog.__init__ with args () {'title': 'A Propos Settings'}\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
    #         "called FlexGridSizer.__init__ with args () {'cols': 2}\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL | testee.wx.ALIGN_CENTER_VERTICAL}"
    #         ", 5)\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_APPLY}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         f"called dialog.SetAffirmativeId with args ({testee.wx.ID_APPLY},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_CLOSE}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         f"called dialog.SetEscapeId with args ({testee.wx.ID_CLOSE},)\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL | testee.wx.ALIGN_CENTER_VERTICAL}"
    #         ", 5)\n"
    #         "called dialog.SetSizer with args (vert sizer,)\n"
    #         "called dialog.SetAutoLayout with args (True,)\n"
    #         f"called vert sizer.Fit with args ({testobj},)\n"
    #         f"called vert sizer.SetSizeHints with args ({testobj},)\n"
    #         "called dialog.Layout with args ()\n")

    #     parent.opts = {'x': 'y', 'a': 'b'}
    #     testobj = testee.OptionsDialog(parent, 'title')
    #     assert testobj.controls == []
    #     assert capsys.readouterr().out == (
    #         "called Dialog.__init__ with args () {'title': 'A Propos Settings'}\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
    #         "called FlexGridSizer.__init__ with args () {'cols': 2}\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL | testee.wx.ALIGN_CENTER_VERTICAL}"
    #         ", 5)\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_APPLY}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         f"called dialog.SetAffirmativeId with args ({testee.wx.ID_APPLY},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_CLOSE}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         f"called dialog.SetEscapeId with args ({testee.wx.ID_CLOSE},)\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL | testee.wx.ALIGN_CENTER_VERTICAL}"
    #         ", 5)\n"
    #         "called dialog.SetSizer with args (vert sizer,)\n"
    #         "called dialog.SetAutoLayout with args (True,)\n"
    #         f"called vert sizer.Fit with args ({testobj},)\n"
    #         f"called vert sizer.SetSizeHints with args ({testobj},)\n"
    #         "called dialog.Layout with args ()\n")

    #     testobj = testee.OptionsDialog(parent, 'title', sett2text={'x': 'xxx', 'a': 'aaa'})
    #     assert testobj.controls[0][0] == 'x'
    #     assert isinstance(testobj.controls[0][1], testee.wx.CheckBox)
    #     assert testobj.controls[1][0] == 'a'
    #     assert isinstance(testobj.controls[1][1], testee.wx.CheckBox)
    #     assert capsys.readouterr().out == (
    #         "called Dialog.__init__ with args () {'title': 'A Propos Settings'}\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
    #         "called FlexGridSizer.__init__ with args () {'cols': 2}\n"
    #         f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
    #         f"called FlexGridSizer.Add with args <item> (1, {testee.wx.ALL}, 5)\n"
    #         f"called CheckBox.__init__ with args ({testobj},) {{}}\n"
    #         "called checkbox.SetValue with args ('y',)\n"
    #         f"called FlexGridSizer.Add with args <item> (1, {testee.wx.ALL}, 5)\n"
    #         f"called StaticText.__init__ with args ({testobj},) {{'label': 'aaa'}}\n"
    #         f"called FlexGridSizer.Add with args <item> (1, {testee.wx.ALL}, 5)\n"
    #         f"called CheckBox.__init__ with args ({testobj},) {{}}\n"
    #         "called checkbox.SetValue with args ('b',)\n"
    #         f"called FlexGridSizer.Add with args <item> (1, {testee.wx.ALL}, 5)\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL | testee.wx.ALIGN_CENTER_VERTICAL}"
    #         ", 5)\n"
    #         f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_APPLY}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         f"called dialog.SetAffirmativeId with args ({testee.wx.ID_APPLY},)\n"
    #         f"called Button.__init__ with args ({testobj},) {{'id': {testee.wx.ID_CLOSE}}}\n"
    #         f"called hori sizer.Add with args <item> (0, {testee.wx.EXPAND | testee.wx.ALL}, 2)\n"
    #         f"called dialog.SetEscapeId with args ({testee.wx.ID_CLOSE},)\n"
    #         "called vert sizer.Add with args <item> (0,"
    #         f" {testee.wx.ALL | testee.wx.ALIGN_CENTER_HORIZONTAL | testee.wx.ALIGN_CENTER_VERTICAL}"
    #         ", 5)\n"
    #         "called dialog.SetSizer with args (vert sizer,)\n"
    #         "called dialog.SetAutoLayout with args (True,)\n"
    #         f"called vert sizer.Fit with args ({testobj},)\n"
    #         f"called vert sizer.SetSizeHints with args ({testobj},)\n"
    #         "called dialog.Layout with args ()\n")

    # def test_accept(self, monkeypatch, capsys):
    #     """unittest for OptionsDialog.accept
    #     """
    #     c1 = mockwx.MockCheckBox()
    #     c1.SetValue(True)
    #     c2 = mockwx.MockCheckBox()
    #     c2.SetValue(False)
    #     assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
    #                                        "called checkbox.SetValue with args (True,)\n"
    #                                        "called CheckBox.__init__ with args () {}\n"
    #                                        "called checkbox.SetValue with args (False,)\n")
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.parent = types.SimpleNamespace(opts={})
    #     testobj.controls = []
    #     testobj.accept()
    #     assert testobj.parent.opts == {}
    #     testobj.parent = types.SimpleNamespace(opts={'x': False, 'y': True})
    #     testobj.controls = [('x', c1), ('y', c2)]
    #     testobj.accept()
    #     assert testobj.parent.opts == {'x': True, 'y': False}
    def test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.init
        """
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        testobj = testee.OptionsDialog('master', 'parent')
        assert testobj.master == 'master'
        assert testobj.parent == 'parent'
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert isinstance(testobj.gsizer, testee.wx.FlexGridSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'Apropos'}\n"
                f'called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n'
                "called GridSizer.__init__ with args () {'cols': 2}\n"
                "called vert sizer.Add with args <item> (0, 2544, 5)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for OptionsDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
        testobj = testee.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_checkbox_line_to_grid(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_checkbox_line_to_grid
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_checkbox_line_to_grid(1, 'xxx', 'yyy')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called GridSizer.Add with args <item> (1, 240, 5)\n"
                f"called CheckBox.__init__ with args ({testobj},) {{}}\n"
                "called checkbox.SetValue with args ('yyy',)\n"
                "called GridSizer.Add with args <item> (1, 240, 5)\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_buttonbox
        """
        def mock_set(arg):
            print(f'called OptionsDialog.SetEscapeId with arg {arg}')
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetEscapeId = mock_set
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_buttonbox('xxx', 'yyy')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100, 'label': 'xxx'}}\n"
                "called hori sizer.Add with args <item> (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5001, 'label': 'yyy'}}\n"
                "called hori sizer.Add with args <item> (0, 8432, 2)\n"
                "called OptionsDialog.SetEscapeId with arg 5001\n"
                "called vert sizer.Add with args <item> (0, 2544, 5)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for OptionsDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        check.SetValue(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")
