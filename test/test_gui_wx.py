"""unittests for ./apropos/gui_wx.py
"""
from mockgui import mockwxwidgets as mockwx
from apropos import gui_wx as testee

def setup_mainwindow(monkeypatch, capsys):
    """stub for setting up MainWindow object
    """
    monkeypatch.setattr(testee.wx, 'Frame', mockwx.MockFrame)
    monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
    testobj = gui.MainWindow(MockApropos())
    assert capsys.readouterr().out == ('called NoteTree.__init__()\n'
                                       'called app.__init__()\n')
    return testobj


class MockApropos:
    def __init__(self):
        print("called Apropos.__init__")


class TestAproposGui:
    """unittest for gui_wx.AproposGui
    """

    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.AproposGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AproposGui.__init__ with args', args)
        testobj = testee.AproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AproposGui.__init__
        """
        # monkeypatch.setattr(testee.wx, 'Frame', mockwx.MockFrame)
        monkeypatch.setattr(testee.wx.Frame, '__init__', mockwx.MockFrame.__init__)
        # monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
        monkeypatch.setattr(testee.wx.App, '__init__', mockwx.MockApp.__init__)
        testparent = MockApropos()
        assert capsys.readouterr().out == 'called Apropos.__init__\n'
        testobj = testee.AproposGui(testparent, parent=None)  # , fname='', title='Apropos')
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'

    def _test_set_appicon(self, monkeypatch, capsys):
        """unittest for AproposGui.set_appicon
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_appicon(self, iconame) == "expected_result"

    def _test_init_trayicon(self, monkeypatch, capsys):
        """unittest for AproposGui.init_trayicon
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.init_trayicon(self, iconame, tooltip) == "expected_result"

    def _test_setup_tabwidget(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_tabwidget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.setup_tabwidget(self, change_page, close_page) == "expected_result"

    def _test_setup_shortcuts(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_shortcuts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.setup_shortcuts(self, handler_dict) == "expected_result"

    def _test_go(self, monkeypatch, capsys):
        """unittest for AproposGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.go(self) == "expected_result"

    def _test_get_page_count(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_count
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_page_count(self) == "expected_result"

    def _test_get_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.get_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_current_page(self):  #  , event=None) == "expected_result"

    def _test_set_previous_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_previous_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_previous_page(self) == "expected_result"

    def _test_set_next_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_next_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_next_page(self) == "expected_result"

    def _test_set_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_current_page(self, page_number) == "expected_result"

    def _test_set_focus_to_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_focus_to_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_focus_to_page(self, event=None) == "expected_result"

    def _test_clear_all(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.clear_all(self) == "expected_result"

    def _test_new_page(self, monkeypatch, capsys):
        """unittest for AproposGui.new_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.new_page(self, nieuw, titel, note) == "expected_result"

    def _test_clear_last_page(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_last_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.clear_last_page(self) == "expected_result"

    def _test_delete_page(self, monkeypatch, capsys):
        """unittest for AproposGui.delete_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.delete_page(self, page_number) == "expected_result"

    def _test_hide_app(self, monkeypatch, capsys):
        """unittest for AproposGui.hide_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.hide_app(self) == "expected_result"

    def _test_reshow_app(self, monkeypatch, capsys):
        """unittest for AproposGui.reshow_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.reshow_app(self, event=None) == "expected_result"

    def _test_get_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_page_title(self, pageno) == "expected_result"

    def _test_get_page_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_page_text(self, pageno) == "expected_result"

    def _test_meld(self, monkeypatch, capsys):
        """unittest for AproposGui.meld
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.meld(self, text) == "expected_result"

    def _test_show_dialog(self, monkeypatch, capsys):
        """unittest for AproposGui.show_dialog
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.show_dialog(self, cls, options) == "expected_result"

    def _test_get_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_text(self, prompt, initial='') == "expected_result"

    def _test_set_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_page_title(self, pageno, title) == "expected_result"

    def _test_get_item(self, monkeypatch, capsys):
        """unittest for AproposGui.get_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_item(self, prompt, itemlist, initial=None) == "expected_result"

    def _test_on_left_doubleclick(self, monkeypatch, capsys):
        """unittest for AproposGui.on_left_doubleclick
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.on_left_doubleclick(self, event=None) == "expected_result"

    def _test_close(self, monkeypatch, capsys):
        """unittest for AproposGui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.close(self, event=None) == "expected_result"


class _TestPage:
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
        testobj = testee.Page()
        assert capsys.readouterr().out == 'called Page.__init__ with args ()\n'
        return testobj

    def _test___init__(self, monkeypatch, capsys):
        """unittest for Page.__init__
        """
        testobj = testee.Page()
        assert capsys.readouterr().out == 'called Page.__init__ with args ()'
        # assert testobj.__init__(self, parent) == "expected_result"


class _TestCheckDialog:
    """unittest for gui_wx.CheckDialog
    """

    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.CheckDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CheckDialog.__init__ with args', args)
        testobj = testee.CheckDialog()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()\n'
        return testobj

    def _test___init__(self, monkeypatch, capsys):
        """unittest for CheckDialog.__init__
        """
        testobj = testee.CheckDialog()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title, message="", option="", caption=True) == "expected_result"

    def _test_accept(self, monkeypatch, capsys):
        """unittest for CheckDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()'
        # assert testobj.accept(self) == "expected_result"


class _TestTaskbarIcon:
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
        testobj = testee.TaskbarIcon()
        assert capsys.readouterr().out == 'called TaskbarIcon.__init__ with args ()\n'
        return testobj

    def _test___init__(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.__init__
        """
        testobj = testee.TaskbarIcon()
        assert capsys.readouterr().out == 'called TaskbarIcon.__init__ with args ()'
        # assert testobj.__init__(self, parent, iconame) == "expected_result"

    def _test_CreatePopupMenu(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.CreatePopupMenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called TaskbarIcon.__init__ with args ()'
        # assert testobj.CreatePopupMenu(self) == "expected_result"


class _TestOptionsDialog:
    """unittest for gui_wx.OptionsDialog
    """

    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.OptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called OptionsDialog.__init__ with args', args)
        testobj = testee.OptionsDialog()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()\n'
        return testobj

    def _test___init__(self, monkeypatch, capsys):
        """unittest for OptionsDialog.__init__
        """
        testobj = testee.OptionsDialog()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title, sett2text=None) == "expected_result"

    def _test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()'
        # assert testobj.accept(self) == "expected_result"
