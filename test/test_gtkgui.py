"""unittests for ./apropos/gui_gtk.py
"""
from apropos import gui_gtk as testee


def _test_convert2gtk(monkeypatch, capsys):
    """unittest for gui_gtk.convert2gtk
    """
    assert testee.convert2gtk(accel) == "expected_result"


class TestAproposGui:
    """unittest for gui_gtk.AproposGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_gtk.AproposGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AproposGui.__init__ with args', args)
        monkeypatch.setattr(testee.AproposGui, '__init__', mock_init)
        testobj = testee.AproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for AproposGui.__init__
        """
        testobj = testee.AproposGui(master, title='')
        assert capsys.readouterr().out == ("")

    def _test_do_activate(self, monkeypatch, capsys):
        """unittest for AproposGui.do_activate
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_activate() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for AproposGui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close(action, param) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_appicon(self, monkeypatch, capsys):
        """unittest for AproposGui.set_appicon
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_appicon(iconame) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_trayicon(self, monkeypatch, capsys):
        """unittest for AproposGui.init_trayicon
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_trayicon(iconame, tooltip) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_tabwidget(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_tabwidget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_tabwidget(change_page, close_page) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_shortcuts(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_shortcuts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_shortcuts(shortcut_dict) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for AproposGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page_count(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_count
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_count() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.get_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_current_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_previous_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_previous_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_previous_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_next_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_next_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_next_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_current_page(pageno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus_to_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_focus_to_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus_to_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_all(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_all() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_new_page(self, monkeypatch, capsys):
        """unittest for AproposGui.new_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.new_page(nieuw, titel, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_last_page(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_last_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_last_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_page(self, monkeypatch, capsys):
        """unittest for AproposGui.delete_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_page(pagetodelete) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_hide_app(self, monkeypatch, capsys):
        """unittest for AproposGui.hide_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.hide_app() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reshow_app(self, monkeypatch, capsys):
        """unittest for AproposGui.reshow_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reshow_app(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_title(pageno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_text(pageno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meld(self, monkeypatch, capsys):
        """unittest for AproposGui.meld
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meld(meld) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_dialog(self, monkeypatch, capsys):
        """unittest for AproposGui.show_dialog
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_dialog(cls, kwargs) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text(prompt, initial='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_page_title(pageno, title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item(self, monkeypatch, capsys):
        """unittest for AproposGui.get_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item(prompt, itemlist, initial=0) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestMainWin:
    """unittest for gui_gtk.MainWin
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_gtk.MainWin object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainWin.__init__ with args', args)
        monkeypatch.setattr(testee.MainWin, '__init__', mock_init)
        testobj = testee.MainWin()
        assert capsys.readouterr().out == 'called MainWin.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainWin.__init__
        """
        testobj = testee.MainWin(application, title='')
        assert capsys.readouterr().out == ("")

    def _test_set_appicon(self, monkeypatch, capsys):
        """unittest for MainWin.set_appicon
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_appicon(iconame) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_trayicon(self, monkeypatch, capsys):
        """unittest for MainWin.init_trayicon
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_trayicon(iconame, tooltip) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_tabwidget(self, monkeypatch, capsys):
        """unittest for MainWin.setup_tabwidget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_tabwidget(change_page, close_page) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_page_changed(self, monkeypatch, capsys):
        """unittest for MainWin.page_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.page_changed(nb, page, page_num) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_shortcuts(self, monkeypatch, capsys):
        """unittest for MainWin.setup_shortcuts
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_shortcuts(shortcut_dict) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page_count(self, monkeypatch, capsys):
        """unittest for MainWin.get_page_count
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_count() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_current_page(self, monkeypatch, capsys):
        """unittest for MainWin.get_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_current_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_previous_page(self, monkeypatch, capsys):
        """unittest for MainWin.set_previous_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_previous_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_next_page(self, monkeypatch, capsys):
        """unittest for MainWin.set_next_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_next_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_current_page(self, monkeypatch, capsys):
        """unittest for MainWin.set_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_current_page(pageno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus_to_page(self, monkeypatch, capsys):
        """unittest for MainWin.set_focus_to_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus_to_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_all(self, monkeypatch, capsys):
        """unittest for MainWin.clear_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_all() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_new_page(self, monkeypatch, capsys):
        """unittest for MainWin.new_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.new_page(nieuw, titel, note) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_last_page(self, monkeypatch, capsys):
        """unittest for MainWin.clear_last_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_last_page() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_page(self, monkeypatch, capsys):
        """unittest for MainWin.delete_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_page(pagetodelete) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_hide_app(self, monkeypatch, capsys):
        """unittest for MainWin.hide_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.hide_app() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_reshow_app(self, monkeypatch, capsys):
        """unittest for MainWin.reshow_app
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.reshow_app(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page_title(self, monkeypatch, capsys):
        """unittest for MainWin.get_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_title(pageno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_page_text(self, monkeypatch, capsys):
        """unittest for MainWin.get_page_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_text(pageno) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_text(self, monkeypatch, capsys):
        """unittest for MainWin.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text(prompt, initial='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_page_title(self, monkeypatch, capsys):
        """unittest for MainWin.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_page_title(pageno, text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item(self, monkeypatch, capsys):
        """unittest for MainWin.get_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item(prompt, itemlist, initial=0) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for MainWin.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close(*args) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestPage:
    """unittest for gui_gtk.Page
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_gtk.Page object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Page.__init__ with args', args)
        monkeypatch.setattr(testee.Page, '__init__', mock_init)
        testobj = testee.Page()
        assert capsys.readouterr().out == 'called Page.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Page.__init__
        """
        testobj = testee.Page(parent)
        assert capsys.readouterr().out == ("")


class TestCheckDialog:
    """unittest for gui_gtk.CheckDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_gtk.CheckDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CheckDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
        testobj = testee.CheckDialog()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.__init__
        """
        testobj = testee.CheckDialog(parent, title, message="", option="", caption="")
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for CheckDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestOptionsDialog:
    """unittest for gui_gtk.OptionsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_gtk.OptionsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called OptionsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
        testobj = testee.OptionsDialog()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.__init__
        """
        testobj = testee.OptionsDialog(parent, sett2text)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestInputDialog:
    """unittest for gui_gtk.InputDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_gtk.InputDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called InputDialog.__init__ with args', args)
        monkeypatch.setattr(testee.InputDialog, '__init__', mock_init)
        testobj = testee.InputDialog()
        assert capsys.readouterr().out == 'called InputDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for InputDialog.__init__
        """
        testobj = testee.InputDialog(parent, title="")
        assert capsys.readouterr().out == ("")

    def _test_get_text(self, monkeypatch, capsys):
        """unittest for InputDialog.get_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text(title="", caption="Enter some text", text="") == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_item(self, monkeypatch, capsys):
        """unittest for InputDialog.get_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item(title="", caption="Choose an item", items=None, default=0) == "expected_result"
        assert capsys.readouterr().out == ("")
