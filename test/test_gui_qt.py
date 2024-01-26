"""unittests for ./apropos/gui_qt.py
"""
from apropos import gui_qt as testee
from mockwidgets import mockqtwidgets as mockqtw


class MockAproposGui():
    """stub for gui_qt.AproposGui object
    """
    def __init__(self, *args):
        """stub
        """
        print('called AproposGui.__init__ with args', args)


class TestAproposGui:
    """unittest for gui_qt.AproposGui
    """
    def test___init__(self, monkeypatch, capsys):
        """unittest for AproposGui.__init__
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.__init__(self, master, title='Apropos') == expected_result

    def test_set_appicon(self, monkeypatch, capsys):
        """unittest for AproposGui.set_appicon
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_appicon(self, iconame) == expected_result

    def test_init_trayicon(self, monkeypatch, capsys):
        """unittest for AproposGui.init_trayicon
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.init_trayicon(self, iconame, tooltip) == expected_result

    def test_setup_tabwidget(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_tabwidget
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.setup_tabwidget(self, change_page, close_page) == expected_result

    def test_setup_shortcuts(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_shortcuts
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.setup_shortcuts(self, handler_dict) == expected_result

    def test_go(self, monkeypatch, capsys):
        """unittest for AproposGui.go
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.go(self) == expected_result

    def test_get_page_count(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_count
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_page_count(self) == expected_result

    def test_get_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.get_current_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_current_page(self, *args) == expected_result

    def test_set_previous_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_previous_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_previous_page(self) == expected_result

    def test_set_next_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_next_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_next_page(self) == expected_result

    def test_set_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_current_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_current_page(self, page_number) == expected_result

    def test_set_focus_to_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_focus_to_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_focus_to_page(self) == expected_result

    def test_clear_all(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_all
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.clear_all(self) == expected_result

    def test_new_page(self, monkeypatch, capsys):
        """unittest for AproposGui.new_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.new_page(self, nieuw, titel, note) == expected_result

    def test_clear_last_page(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_last_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.clear_last_page(self) == expected_result

    def test_delete_page(self, monkeypatch, capsys):
        """unittest for AproposGui.delete_page
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.delete_page(self, pagetodelete) == expected_result

    def test_closeEvent(self, monkeypatch, capsys):
        """unittest for AproposGui.closeEvent
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.closeEvent(self, event) == expected_result

    def test_hide_app(self, monkeypatch, capsys):
        """unittest for AproposGui.hide_app
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.hide_app(self) == expected_result

    def test_reshow_app(self, monkeypatch, capsys):
        """unittest for AproposGui.reshow_app
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.reshow_app(self, event) == expected_result

    def test_get_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_title
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_page_title(self, pageno) == expected_result

    def test_get_page_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_text
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_page_text(self, pageno) == expected_result

    def test_meld(self, monkeypatch, capsys):
        """unittest for AproposGui.meld
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.meld(self, meld) == expected_result

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for AproposGui.show_dialog
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.show_dialog(self, cls, kwargs) == expected_result

    def test_get_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_text
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_text(self, prompt, initial='') == expected_result

    def test_set_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.set_page_title
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.set_page_title(self, pageno, title) == expected_result

    def test_get_item(self, monkeypatch, capsys):
        """unittest for AproposGui.get_item
        """
        testobj = MockAproposGui()
        assert capsys.readouterr().out == 'called AproposGui.__init__ with args ()'
        # assert testobj.get_item(self, prompt, itemlist, initial=0) == expected_result


class MockPage():
    """stub for gui_qt.Page object
    """
    def __init__(self, *args):
        """stub
        """
        print('called Page.__init__ with args', args)


class TestPage:
    """unittest for gui_qt.Page
    """
    def test___init__(self, monkeypatch, capsys):
        """unittest for Page.__init__
        """
        testobj = MockPage()
        assert capsys.readouterr().out == 'called Page.__init__ with args ()'
        # assert testobj.__init__(self, parent) == expected_result


class MockCheckDialog():
    """stub for gui_qt.CheckDialog object
    """
    def __init__(self, *args):
        """stub
        """
        print('called CheckDialog.__init__ with args', args)


class TestCheckDialog:
    """unittest for gui_qt.CheckDialog
    """
    def test___init__(self, monkeypatch, capsys):
        """unittest for CheckDialog.__init__
        """
        testobj = MockCheckDialog()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title, message="", option="", caption=True) == expected_result

    def test_klaar(self, monkeypatch, capsys):
        """unittest for CheckDialog.klaar
        """
        testobj = MockCheckDialog()
        assert capsys.readouterr().out == 'called CheckDialog.__init__ with args ()'
        # assert testobj.klaar(self) == expected_result


class MockOptionsDialog():
    """stub for gui_qt.OptionsDialog object
    """
    def __init__(self, *args):
        """stub
        """
        print('called OptionsDialog.__init__ with args', args)


class TestOptionsDialog:
    """unittest for gui_qt.OptionsDialog
    """
    def test___init__(self, monkeypatch, capsys):
        """unittest for OptionsDialog.__init__
        """
        testobj = MockOptionsDialog()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()'
        # assert testobj.__init__(self, parent, title, sett2text=None) == expected_result

    def test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        testobj = MockOptionsDialog()
        assert capsys.readouterr().out == 'called OptionsDialog.__init__ with args ()'
        # assert testobj.accept(self) == expected_result
