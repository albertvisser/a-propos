"""unittests for ./apropos/gui_qt.py
"""
import types
import pytest
from apropos import gui_qt as testee
from mockgui import mockqtwidgets as mockqtw

# output predictions
page_output = """\
called Frame.__init__
called Editor.__init__ with args ({testobj},)
called VBox.__init__
called HBox.__init__
called HBox.addWidget with arg MockEditorWidget
called VBox.addLayout with arg MockHBoxLayout
called Frame.setLayout with arg MockVBoxLayout
"""
checkdialog_output = """\
called Dialog.__init__ with args {testparent} () {{}}
called Dialog.setWindowTitle with args ('title',)
called Dialog.setWindowIcon with args ('Icon',)
called Editor.__init__ with args ('x',)
called CheckBox.__init__ with text '{checktitle}'
called CheckBox.setChecked with arg {checked}
called PushButton.__init__ with args ('&Ok', {testobj}) {{}}
called Signal.connect with args ({testobj.klaar},)
called VBox.__init__
called HBox.__init__
called HBox.addWidget with arg MockEditorWidget
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addWidget with arg MockCheckBox
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addWidget with arg MockPushButton
called HBox.insertStretch
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Dialog.setLayout
called Dialog.exec
"""
optionsdialog_start = """\
called Dialog.__init__ with args {testparent} () {{}}
called Dialog.setWindowTitle with args ('title',)
called Dialog.setWindowIcon with args ('Icon',)
called VBox.__init__
called Grid.__init__
"""
optionsdialog_middle = """\
called Editor.__init__ with args ('yyyy', {testobj})
called Grid.addWidget with arg MockEditorWidget at (1, 0)
called CheckBox.__init__ with text ''
called CheckBox.setChecked with arg False
called Grid.addWidget with arg MockCheckBox at (1, 1)
called Editor.__init__ with args ('zzzz', {testobj})
called Grid.addWidget with arg MockEditorWidget at (2, 0)
called CheckBox.__init__ with text ''
called CheckBox.setChecked with arg True
called Grid.addWidget with arg MockCheckBox at (2, 1)
"""
optionsdialog_end = """\
called VBox.addLayout with arg MockGridLayout
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Apply', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Close', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Dialog.setLayout
called Dialog.exec
"""

@pytest.fixture
def expected_output():
    """fixture for output predictions
    """
    return {"page": page_output,
            "checkdialog": checkdialog_output,
            "optionsdialog": optionsdialog_start + optionsdialog_end,
            "optionsdialog_w_options": optionsdialog_start + optionsdialog_middle + optionsdialog_end}


class MockApropos():
    """stub for gui_qt.Apropos object
    """
    def __init__(self, *args):
        """stub
        """
        print('called Apropos.__init__')
    def revive(self, *args):
        """stub, needed only for the reference to the method
        """
    def afsl(self, *args):
        """stub
        """
        print('called Apropos.afsl')


class MockPage():
    """stub for gui_qt.Page object
    """
    def __init__(self, *args):
        """stub
        """
        print('called Page.__init__')
        self.txt = mockqtw.MockEditorWidget()
    def __str__(self):
        return 'A Page'
    def destroy(self):
        print('called.Page.destroy')


class TestAproposGui:
    """unittest for gui_qt.AproposGui
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for AproposGui.__init__
        """
        def mock_init(self, *args, **kwargs):
            print('called MainWindow.__init__')
        def mock_app_init(self, *args, **kwargs):
            print('called Application.__init__')
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        testobj = testee.AproposGui('master')
        assert testobj.master == 'master'
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert isinstance(testobj, testee.qtw.QMainWindow)
        assert capsys.readouterr().out == ('called Application.__init__\n'
                                           'called MainWindow.__init__\n'
                                           'called MainWindow.setWindowTitle with arg `Apropos`\n'
                                           'called MainWindow.move with args (10, 10)\n'
                                           'called MainWindow.resize with args (650, 400)\n')
        monkeypatch.setattr(testee.sys, 'platform', 'win')
        testobj = testee.AproposGui('master', 'testgui')
        assert testobj.master == 'master'
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert isinstance(testobj, testee.qtw.QMainWindow)
        assert capsys.readouterr().out == ('called Application.__init__\n'
                                           'called MainWindow.__init__\n'
                                           'called MainWindow.setWindowTitle with arg `testgui`\n'
                                           'called MainWindow.move with args (30, 30)\n'
                                           'called MainWindow.resize with args (650, 400)\n')

    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui.AproposGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that methods can be monkeypatched in the caller
        """
        def mock_init(self, *args, **kwargs):
            print('called AproposGui.__init__')
        monkeypatch.setattr(testee.AproposGui, '__init__', mock_init)
        testobj = testee.AproposGui()
        testobj.master = MockApropos()
        testobj.app = mockqtw.MockApplication()
        testobj.nb = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == ('called AproposGui.__init__\n'
                                           'called Apropos.__init__\n'
                                           'called Application.__init__\n'
                                           'called TabWidget.__init__\n')
        return testobj

    def test_set_appicon(self, monkeypatch, capsys):
        """unittest for AproposGui.set_appicon
        """
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'setWindowIcon', mockqtw.MockMainWindow.setWindowIcon)
        testobj.set_appicon('iconame')
        assert capsys.readouterr().out == ('called Icon.__init__ with arg `iconame`\n'
                                           'called MainWindow.setWindowIcon\n')

    def test_init_trayicon(self, monkeypatch, capsys):
        """unittest for AproposGui.init_trayicon
        """
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw, 'QSystemTrayIcon', mockqtw.MockSysTrayIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.revive = lambda: 0
        testobj.init_trayicon('iconame', 'tooltip')
        assert capsys.readouterr().out == (
                "called Icon.__init__ with arg `iconame`\n"
                "called TrayIcon.__init__\n"
                "called TrayIcon.setToolTip with args ('Click to revive Apropos',)\n"
                f"called Signal.connect with args ({testobj.master.revive},)\n"
                "called TrayIcon.hide\n")

    def test_setup_tabwidget(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_tabwidget
        """
        def change_page():
            """stub
            """
        def close_page():
            """stub
            """
        def mock_setwidget(arg):
            """stub
            """
            print('called AproposGui.setCentralWidget with arg', arg)
        monkeypatch.setattr(testee.qtw, 'QTabWidget', mockqtw.MockTabWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'setCentralWidget', mock_setwidget)
        testobj.setup_tabwidget(change_page, close_page)
        assert capsys.readouterr().out == (
                'called TabWidget.__init__\n'
                f'called AproposGui.setCentralWidget with arg {testobj.nb}\n'
                f'called Signal.connect with args ({change_page},)\n'
                f'called Signal.connect with args ({close_page},)\n')

    def test_setup_shortcuts(self, monkeypatch, capsys):
        """unittest for AproposGui.setup_shortcuts
        """
        def mock_add(arg):
            "stub"
            print('called AproposGui.addAction')
        def handler1(arg):
            "stub, alleen nodig voor reference naar functie"
        def handler2(arg):
            "stub, alleen nodig voor reference naar functie"
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'addAction', mock_add)
        testobj.setup_shortcuts({'lbl1': (('x', 'y'), handler1), 'lbl2': (('zx',), handler2)})
        assert capsys.readouterr().out == (f"called Action.__init__ with args ('lbl1', {testobj})\n"
                                           "called Action.setShortcuts with arg `['x', 'y']`\n"
                                           f"called Signal.connect with args ({handler1},)\n"
                                           "called AproposGui.addAction\n"
                                           f"called Action.__init__ with args ('lbl2', {testobj})\n"
                                           "called Action.setShortcuts with arg `['zx']`\n"
                                           f"called Signal.connect with args ({handler2},)\n"
                                           "called AproposGui.addAction\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for AproposGui.go
        """
        def mock_show():
            print('called AproposGui.show')
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'show', mock_show)
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == "called AproposGui.show\ncalled Application.exec\n"

    def test_get_page_count(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_count
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_page_count() == "number of tabs"
        assert capsys.readouterr().out == 'called TabWidget.count\n'

    def test_get_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.get_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_current_page() == -1
        assert capsys.readouterr().out == 'called TabWidget.currentIndex\n'

    def test_set_previous_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_previous_page
        """
        def mock_set_page(arg):
            """stub
            """
            print(f'called AproposGui.set_current_page with arg `{arg}`')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_current_page = mock_set_page
        testobj.master.current = 2
        testobj.set_previous_page()
        assert capsys.readouterr().out == 'called AproposGui.set_current_page with arg `1`\n'
        testobj.master.current = 1
        testobj.set_previous_page()
        assert capsys.readouterr().out == 'called AproposGui.set_current_page with arg `0`\n'
        testobj.master.current = 0
        testobj.set_previous_page()
        assert capsys.readouterr().out == ''

    def test_set_next_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_next_page
        """
        def mock_set_page(arg):
            """stub
            """
            print(f'called AproposGui.set_current_page with arg `{arg}`')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_current_page = mock_set_page
        monkeypatch.setattr(testobj.nb, 'count', lambda: 2)
        testobj.master.current = 0
        testobj.set_next_page()
        assert capsys.readouterr().out == 'called AproposGui.set_current_page with arg `1`\n'
        testobj.master.current = 1
        testobj.set_next_page()
        assert capsys.readouterr().out == 'called AproposGui.set_current_page with arg `2`\n'
        testobj.master.current = 2
        testobj.set_next_page()
        assert capsys.readouterr().out == ''

    def test_set_current_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_current_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_current_page(1)
        assert capsys.readouterr().out == 'called TabWidget.setCurrentIndex with arg `1`\n'

    def test_set_focus_to_page(self, monkeypatch, capsys):
        """unittest for AproposGui.set_focus_to_page
        """
        def mock_current():
            print('called TabWidget.currentWidget')
            return MockPage()
        def mock_current_2():
            print('called TabWidget.currentWidget')
            return None
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb.currentWidget = mock_current
        testobj.set_focus_to_page()
        assert capsys.readouterr().out == ('called TabWidget.currentWidget\n'
                                           'called Page.__init__\n'
                                           'called Editor.__init__\n'
                                           'called Editor.setFocus\n')
        testobj.nb.currentWidget = mock_current_2
        testobj.set_focus_to_page()
        assert capsys.readouterr().out == 'called TabWidget.currentWidget\n'

    def test_clear_all(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_all
        """
        def mock_count():
            print('called TabWidget.count')
            return 2
        def mock_widget(arg):
            print(f'called TabWidget.widget with arg `{arg}`')
            return MockPage()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb.count = mock_count
        testobj.nb.widget = mock_widget
        testobj.clear_all()
        assert capsys.readouterr().out == ('called TabWidget.count\n'
                                           'called TabWidget.widget with arg `0`\n'
                                           'called Page.__init__\n'
                                           'called Editor.__init__\n'
                                           'called TabWidget.widget with arg `1`\n'
                                           'called Page.__init__\n'
                                           'called Editor.__init__\n'
                                           'called TabWidget.clear\n'
                                           'called.Page.destroy\n'
                                           'called.Page.destroy\n')

    def test_new_page(self, monkeypatch, capsys):
        """unittest for AproposGui.new_page
        """
        monkeypatch.setattr(testee, 'Page', MockPage)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockqtw.MockTabWidget()
        assert capsys.readouterr().out == "called TabWidget.__init__\n"
        testobj.new_page(1, 'titel')
        assert capsys.readouterr().out == ("called Page.__init__\n"
                                           "called Editor.__init__\n"
                                           "called TabWidget.addTab with args `A Page` `titel`\n"
                                           "called TabWidget.setCurrentIndex with arg `1`\n"
                                           "called TabWidget.setCurrentWidget with arg `A Page`\n")
        testobj.new_page(2, 'titel', 'note')
        assert capsys.readouterr().out == ("called Page.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Editor.setText with arg `note`\n"
                                           "called TabWidget.addTab with args `A Page` `titel`\n"
                                           "called TabWidget.setCurrentIndex with arg `2`\n"
                                           "called TabWidget.setCurrentWidget with arg `A Page`\n")

    def test_clear_last_page(self, monkeypatch, capsys):
        """unittest for AproposGui.clear_last_page
        """
        def mock_widget(arg):
            print('called TabWidget.widget with arg', arg)
            return MockPage()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb.widget = mock_widget
        testobj.master.current = 1
        testobj.clear_last_page()
        assert capsys.readouterr().out == ("called TabWidget.setTabText with args (1, '1')\n"
                                           "called TabWidget.widget with arg 1\n"
                                           "called Page.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Editor.setText with arg ``\n")

    def test_delete_page(self, monkeypatch, capsys):
        """unittest for AproposGui.delete_page
        """
        def mock_widget(arg):
            print('called TabWidget.widget with arg', arg)
            return MockPage()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb.widget = mock_widget
        testobj.delete_page(1)
        assert capsys.readouterr().out == ('called TabWidget.widget with arg 1\n'
                                           'called Page.__init__\n'
                                           'called Editor.__init__\n'
                                           'called TabWidget.removeTab with arg 1\n'
                                           'called.Page.destroy\n')

    def test_closeEvent(self, monkeypatch, capsys):
        """unittest for AproposGui.closeEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.closeEvent('event')
        assert capsys.readouterr().out == 'called Apropos.afsl\n'

    def test_hide_app(self, monkeypatch, capsys):
        """unittest for AproposGui.hide_app
        """
        def mock_hide():
            print('called AproposGui.hide')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hide = mock_hide
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        testobj.hide_app()
        assert capsys.readouterr().out == ('called TrayIcon.__init__\n'
                                           'called TrayIcon.show\n'
                                           'called AproposGui.hide\n')

    def test_reshow_app(self, monkeypatch, capsys):
        """unittest for AproposGui.reshow_app
        """
        def mock_show():
            print('called AproposGui.show')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show = mock_show
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        assert capsys.readouterr().out == 'called TrayIcon.__init__\n'
        testobj.reshow_app(testee.qtw.QSystemTrayIcon.ActivationReason.Unknown)
        assert capsys.readouterr().out == ("called TrayIcon.showMessage with args ('Apropos',"
                                           " 'Click to revive Apropos')\n")
        testobj.reshow_app(testee.qtw.QSystemTrayIcon.ActivationReason.Context)
        assert capsys.readouterr().out == ("called TrayIcon.showMessage with args ('Apropos',"
                                           " 'Click to revive Apropos')\n")
        testobj.reshow_app('event')
        assert capsys.readouterr().out == ('called AproposGui.show\n'
                                           'called TrayIcon.hide\n')

    def test_get_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockqtw.MockTabWidget()
        assert testobj.get_page_title(1) == "tab text"
        assert capsys.readouterr().out == ('called TabWidget.__init__\n'
                                           'called TabWidget.tabtext with args (1,)\n')

    def test_get_page_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_page_text
        """
        def mock_widget(arg):
            print('called TabWidget.widget with arg', arg)
            return MockPage()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nb = mockqtw.MockTabWidget()
        testobj.nb.widget = mock_widget
        assert testobj.get_page_text(1) == "editor text"
        assert capsys.readouterr().out == ('called TabWidget.__init__\n'
                                           'called TabWidget.widget with arg 1\n'
                                           'called Page.__init__\n'
                                           'called Editor.__init__\n'
                                           'called Editor.toPlainText\n')

    def test_meld(self, monkeypatch, capsys):
        """unittest for AproposGui.meld
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.meld('melding')
        assert capsys.readouterr().out == (f'called MessageBox.information with args `{testobj}`'
                                           ' `Apropos` `melding`\n')

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for AproposGui.show_dialog
        """
        def mock_exec(self):
            print('called Dialog.exec')
            return testee.qtw.QDialog.DialogCode.Rejected
        def mock_exec_2(self):
            print('called Dialog.exec')
            return testee.qtw.QDialog.DialogCode.Accepted
        monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec)
        dlg = mockqtw.MockDialog()
        assert capsys.readouterr().out == "called Dialog.__init__ with args None () {}\n"
        dlg.master = types.SimpleNamespace(dialog_data='data')
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_dialog(dlg) == (False, 'data')
        monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec_2)
        assert testobj.show_dialog(dlg) == (True, 'data')
        # testobj.show_dialog(mockqtw.MockDialog, {'x': 'y'})
        # assert capsys.readouterr().out == (f"called Dialog.__init__ with args {testobj}"
        #                                    " ('Apropos',) {'x': 'y'}\n")

    def test_get_text(self, monkeypatch, capsys):
        """unittest for AproposGui.get_text
        """
        def mock_get(parent, *args, **kwargs):
            print('called InputDialog.getText with args', parent, args, kwargs)
            return 'value', True
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text('prompt_text') == ('', False)
        assert capsys.readouterr().out == (f"called InputDialog.getText with args {testobj}"
                                           " ('Apropos', 'prompt_text') {'text': ''}\n")
        monkeypatch.setattr(mockqtw.MockInputDialog, 'getText', mock_get)
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_text('prompt_text', 'initial text') == ("value", True)
        assert capsys.readouterr().out == (f"called InputDialog.getText with args {testobj}"
                                           " ('Apropos', 'prompt_text') {'text': 'initial text'}\n")

    def test_set_page_title(self, monkeypatch, capsys):
        """unittest for AproposGui.set_page_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_page_title(1, 'page title')
        assert capsys.readouterr().out == ("called TabWidget.setTabText with args"
                                           " (1, 'page title')\n")

    def test_get_item(self, monkeypatch, capsys):
        """unittest for AproposGui.get_item
        """
        def mock_get(parent, *args, **kwargs):
            print('called InputDialog.getItem with args', parent, args, kwargs)
            return 'value', True
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item('prompt_text', ['item', 'list']) == ('', False)
        assert capsys.readouterr().out == (
                f"called InputDialog.getItem with args {testobj}"
                " ('Apropos', 'prompt_text', ['item', 'list'], 0, False) {}\n")
        monkeypatch.setattr(mockqtw.MockInputDialog, 'getItem', mock_get)
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item('prompt_text', ['item', 'list'], initial=1) == ("value", True)
        assert capsys.readouterr().out == (
                f"called InputDialog.getItem with args {testobj}"
                " ('Apropos', 'prompt_text', ['item', 'list'], 1, False) {}\n")

    def test_set_screen_dimensions(self, monkeypatch, capsys):
        """unittest for AproposGui.set_screen_dimensions
        """
        def mock_move(*args):
            print("called AproposGui.move with args", args)
        def mock_resize(*args):
            print("called AproposGui.resize with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.move = mock_move
        testobj.resize = mock_resize
        testobj.set_screen_dimensions('11x12', '200x100')
        assert capsys.readouterr().out == ("called AproposGui.move with args (11, 12)\n"
                                           "called AproposGui.resize with args (200, 100)\n")

    def test_get_screen_dimensions(self, monkeypatch, capsys):
        """unittest for AproposGui.get_screen_dimensions
        """
        def mock_x(*args):
            print("called AproposGui.x")
            return 1
        def mock_y(*args):
            print("called AproposGui.pos")
            return 2
        # def mock_pos(*args):
        #     print("called AproposGui.pos")
        #     return 1, 2
        # def mock_rect(*args):
        #     print("called AproposGui.rect")
        #     return 2, 1
        def mock_width(*args):
            print("called AproposGui.width")
            return 2
        def mock_height(*args):
            print("called AproposGui.height")
            return 1
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.pos = mock_pos
        testobj.x = mock_x
        testobj.y = mock_y
        # testobj.rect = mock_rect
        testobj.width = mock_width
        testobj.height = mock_height
        # assert testobj.get_screen_dimensions() == ('(1, 2)', '(2, 1)')
        assert testobj.get_screen_dimensions() == ('1x2', '2x1')
        assert capsys.readouterr().out == ("called AproposGui.x\n"
                                           "called AproposGui.pos\n"
                                           "called AproposGui.width\n"
                                           "called AproposGui.height\n")


class TestPage:
    """unittest for gui_qt.Page
    """
    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for Page.__init__
        """
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = testee.Page('parent')
        assert capsys.readouterr().out == expected_output["page"].format(testobj=testobj)


class TestCheckDialog:
    """unittest for gui_qt.CheckDialog
    """
    # def test_init(self, monkeypatch, capsys, expected_output):
    #     """unittest for CheckDialog.__init__
    #     """
    #     monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
    #     monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockEditorWidget)
    #     monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
    #     monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    #     monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    #     monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    #     testparent = types.SimpleNamespace(apoicon='Icon',
    #                                        master=types.SimpleNamespace(opts={'y': False}))
    #     testobj = testee.CheckDialog(testparent, 'title', 'x', 'y')
    #     bindings = {'testparent': testparent, 'testobj': testobj, 'checktitle': '',
    #                 'checked': False}
    #     assert capsys.readouterr().out == expected_output['checkdialog'].format(**bindings)

    #     testparent = types.SimpleNamespace(apoicon='Icon',
    #                                        master=types.SimpleNamespace(opts={'y': True}))
    #     testobj = testee.CheckDialog(testparent, 'title', message="x", option="y", caption="z")
    #     bindings = {'testparent': testparent, 'testobj': testobj, 'checktitle': 'z',
    #                 'checked': True}
    #     assert capsys.readouterr().out == expected_output['checkdialog'].format(**bindings)

    # def test_klaar(self, monkeypatch, capsys):
    #     """unittest for CheckDialog.klaar
    #     """
    #     def mock_init(self, *args, **kwargs):
    #         print('called CheckDialog.__init__')
    #         self.parent = args[0]
    #         self.option = kwargs['option']
    #         # super().__init__()
    #     monkeypatch.setattr(testee.qtw.QDialog, 'done', mockqtw.MockDialog.done)
    #     monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
    #     monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
    #     testparent = types.SimpleNamespace(apoicon='Icon',
    #                                        master=types.SimpleNamespace(opts={'y': False}))
    #     # breakpoint()
    #     testobj = testee.CheckDialog(testparent, option='y')
    #     testobj.check = mockqtw.MockCheckBox()
    #     testobj.klaar()
    #     assert capsys.readouterr().out == ('called CheckDialog.__init__\n'
    #                                        'called CheckBox.__init__\n'
    #                                        'called CheckBox.isChecked\n'
    #                                        'called Dialog.done with arg `0`\n')
    def test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.init
        """
        mockparent = types.SimpleNamespace(apoicon='icon')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.CheckDialog('master', mockparent)
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == (
            f'called Dialog.__init__ with args {mockparent} () {{}}\n'
            "called Dialog.setWindowTitle with args ('Apropos',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called VBox.__init__\n'
            'called Dialog.setLayout with arg MockVBoxLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
        testobj = testee.CheckDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_label
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            f"called Label.__init__ with args ('xxx', {testobj})\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_checkbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_checkbox('xxx', True)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            "called CheckBox.__init__ with text 'xxx'\n"
            "called CheckBox.setChecked with arg True\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_ok_buttonbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_ok_buttonbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_ok_buttonbox()
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('&Ok', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.klaar},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for CheckDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockqtw.MockCheckBox()
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_klaar(self, monkeypatch, capsys):
        """unittest for CheckDialog.klaar
        """
        def mock_confirm():
            print('called SetCheck.confirm')
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.klaar()
        assert capsys.readouterr().out == ('called SetCheck.confirm\n'
                                           'called Dialog.accept\n')


class TestOptionsDialog:
    """unittest for gui_qt.OptionsDialog
    """
    # def test_init(self, monkeypatch, capsys, expected_output):
    #     """unittest for OptionsDialog.__init__
    #     """
    #     monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
    #     monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockEditorWidget)
    #     monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
    #     monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
    #     monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    #     monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    #     monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    #     testparent = types.SimpleNamespace(apoicon='Icon',
    #                                        master=types.SimpleNamespace(opts={'y': False, 'z': True}))
    #     testobj = testee.OptionsDialog(testparent, 'title')
    #     assert not testobj.controls
    #     bindings = {'testparent': testparent, 'testobj': testobj}
    #     assert capsys.readouterr().out == expected_output['optionsdialog'].format(**bindings)
    #
    #     testobj = testee.OptionsDialog(testparent, 'title', sett2text={'y': 'yyyy', 'z': 'zzzz'})
    #     assert len(testobj.controls) == 2
    #     assert testobj.controls[0][0] == 'y'
    #     assert isinstance(testobj.controls[0][1], testee.qtw.QCheckBox)
    #     assert testobj.controls[1][0] == 'z'
    #     assert isinstance(testobj.controls[1][1], testee.qtw.QCheckBox)
    #     bindings = {'testparent': testparent, 'testobj': testobj}
    #     assert capsys.readouterr().out == expected_output['optionsdialog_w_options'].format(
    #             **bindings)
    #
    # def test_accept(self, monkeypatch, capsys):
    #     """unittest for OptionsDialog.accept
    #     """
    #     def mock_init(self, *args, **kwargs):
    #         print('called CheckDialog.__init__')
    #         self.parent = args[0]
    #     monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
    #     monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
    #     monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
    #     testparent = types.SimpleNamespace(apoicon='Icon',
    #                                        master=types.SimpleNamespace(opts={'y': False, 'z': True}))
    #     testobj = testee.OptionsDialog(testparent)
    #     assert capsys.readouterr().out == 'called CheckDialog.__init__\n'
    #     check1 = mockqtw.MockCheckBox()
    #     check1.setChecked(True)
    #     assert capsys.readouterr().out == ('called CheckBox.__init__\n'
    #                                        'called CheckBox.setChecked with arg True\n')
    #     check2 = mockqtw.MockCheckBox()
    #     check2.setChecked(False)
    #     assert capsys.readouterr().out == ('called CheckBox.__init__\n'
    #                                        'called CheckBox.setChecked with arg False\n')
    #     testobj.controls = [('y', check1), ('z', check2)]
    #     testobj.accept()
    #     assert testobj.parent.master.opts == {'y': True, 'z': False}
    #     assert capsys.readouterr().out == ('called CheckBox.isChecked\n'
    #                                        'called CheckBox.isChecked\n'
    #                                        'called Dialog.accept\n')
    def test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.init
        """
        mockparent = types.SimpleNamespace(apoicon='icon')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = testee.OptionsDialog('master', mockparent)
        assert testobj.master == 'master'
        assert testobj.parent == mockparent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gbox, testee.qtw.QGridLayout)
        assert capsys.readouterr().out == (
            f'called Dialog.__init__ with args {mockparent} () {{}}\n'
            "called Dialog.setWindowTitle with args ('Apropos',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called VBox.__init__\n'
            'called Grid.__init__\n'
            "called VBox.addLayout with arg MockGridLayout\n"
            'called Dialog.setLayout with arg MockVBoxLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
        testobj = testee.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_checkbox_line_to_grid(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_checkbox_line_to_grid
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_checkbox_line_to_grid(1, 'label', True)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            f"called Label.__init__ with args ('label', {testobj})\n"
            "called Grid.addWidget with arg MockLabel at (1, 0)\n"
            "called CheckBox.__init__ with text ''\n"
            'called CheckBox.setChecked with arg True\n'
            "called Grid.addWidget with arg MockCheckBox at (1, 1)\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_buttonbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.gbox = mockqtw.MockGridLayout()
        testobj.accept = lambda: 'dummy callback'
        testobj.reject = lambda: 'dummy callback'
        assert capsys.readouterr().out == "called VBox.__init__\ncalled Grid.__init__\n"
        testobj.add_buttonbox('yes', 'nooo')
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('yes', {testobj}) {{}}\n"
            f'called Signal.connect with args ({testobj.accept},)\n'
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('nooo', {testobj}) {{}}\n"
            f'called Signal.connect with args ({testobj.reject},)\n'
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for OptionsDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockqtw.MockCheckBox()
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        assert capsys.readouterr().out == ""
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        def mock_confirm():
            print('called SetOptions.confirm')
            return {'text': False}
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ('called SetOptions.confirm\n'
                                           'called Dialog.accept\n')
