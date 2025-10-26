"""unittests for ./apropos/main.py
"""
import types
from apropos import main as testee


class MockApropos:
    """testdouble for main.Apropos object
    """
    def __init__(self, **kwargs):
        print('called Apropos with args', kwargs)
        self.gui = MockAproposGui(self, 'title')
        self.opts = {}
    def newtab(self, **kwargs):
        """stub
        """
        print('called Apropos.newtab with args', kwargs)
    def afsl(self):
        """stub
        """
        print('called Apropos.afsl')


class MockAproposGui:
    """testdouble for gui.AproposGui object
    """
    def __init__(self, master, title):
        self.master = master
        print(f'called AproposGui with title `{title}`')
    def go(self):
        """testdouble
        """
        print('called AproposGui.go')
    def close(self):
        """testdouble
        """
        print('called AproposGui.close')
    def set_appicon(self, name):
        """testdouble
        """
        print(f'called AproposGui.set_appicon with arg `{name}`')
    def init_trayicon(self, *args, **kwargs):
        """testdouble
        """
        print('called AproposGui.init_trayicon with args', args, kwargs)
    def setup_tabwidget(self, *args, **kwargs):
        """testdouble
        """
        print('called AproposGui.setup_tabwidget with args', args, kwargs)
    def setup_shortcuts(self, menudict):
        """testdouble
        """
        # print(f'called AproposGui.setup_shortcuts with arg `{menudict}`')
        # geen argument laten zien spaart een hoop simulatie-opzetten uit
        print('called AproposGui.setup_shortcuts')
    def get_current_page(self):
        """testdouble
        """
        print('called AproposGui.get_current_page')
        return 1
    def set_focus_to_page(self):
        """testdouble
        """
        print('called AproposGui.set_focus_to_page')
    def clear_last_page(self):
        """testdouble
        """
        print('called AproposGui.clear_last_page')
    def clear_all(self):
        """testdouble
        """
        print('called AproposGui.clear_all')
    def hide_app(self):
        """testdouble
        """
        print('called AproposGui.hide_app')
    def set_current_page(self, pageno=None):
        """testdouble
        """
        if pageno is None:
            print('called AproposGui.set_current_page')
        else:
            print(f'called AproposGui.set_current_page with arg `{pageno}`')
    def set_previous_page(self):
        """testdouble
        """
        print('called AproposGui.set_previous_page')
    def set_next_page(self):
        """testdouble
        """
        print('called AproposGui.set_next_page')
    def get_page_count(self):
        """testdouble
        """
        print('called AproposGui.get_page_count')
        return 2
    def new_page(self, *args):
        """testdouble
        """
        print('called AproposGui.new_page with args', args)
    def reshow_app(self, name):
        """testdouble
        """
        print(f'called AproposGui.reshow_app with arg `{name}`')
    def meld(self, msg):
        """testdouble
        """
        print(f'called AproposGui.meld with arg `{msg}`')
    def show_dialog(self, *args):
        """testdouble
        """
        print('called AproposGui.show_dialog with args', args)
        return False, {}
    def get_text(self, **kwargs):
        """testdouble
        """
        print('called AproposGui.get_text with args', kwargs)
        return 'newtext', True
    def get_item(self, **kwargs):
        """testdouble
        """
        print('called AproposGui.get_item with args', kwargs)
        return 'xxx', True
    def get_page_text(self, pagenum):
        """testdouble
        """
        print(f'called AproposGui.get_page_text with arg `{pagenum}`')
        return 'text'
    def get_page_title(self, pagenum):
        """testdouble
        """
        print(f'called AproposGui.get_page_title with arg `{pagenum}`')
        return 'page'
    def set_page_title(self, *args):
        """testdouble
        """
        print('called AproposGui.set_page_title with args', args)
    def delete_page(self, pagenum):
        """testdouble
        """
        print(f'called AproposGui.delete_page with arg `{pagenum}`')


def test_languages():
    """unittest for main.languages
    """
    assert sorted(list(testee.languages)) == ['dutch', 'eng']
    for data in testee.languages.values():
        assert list(data) == ['language', 'info', 'hide_text', 'show_text', 'ask_title',
                              'ask_language', 'load_text', 'save_text', 'ask_hide',
                              'notify_load', 'notify_save']


def test_apropos_function(monkeypatch, capsys):
    """unittest for main.apropos_function
    """
    monkeypatch.setattr(testee, 'Apropos', MockApropos)
    testee.apropos()
    assert capsys.readouterr().out == ("called Apropos with args {'fname': '', 'title': ''}\n"
                                       'called AproposGui with title `title`\n'
                                       'called AproposGui.go\n')
    testee.apropos(fname='x', title='y')
    assert capsys.readouterr().out == ("called Apropos with args {'fname': 'x', 'title': 'y'}\n"
                                       'called AproposGui with title `title`\n'
                                       'called AproposGui.go\n')

def test_apropos_init(monkeypatch, capsys):
    """unittest for main.apropos_init
    """
    def mock_load(fname):
        """stub
        """
        return f'result from dml.get_apofile(`{fname}`)'
    def mock_load_and_set(self):
        """stub
        """
        print('called Apropos.load_and_set_screenpos')
    def mock_initapp(self):
        """stub
        """
        print('called Apropos.initapp')
    monkeypatch.setattr(testee.gui, 'AproposGui', MockAproposGui)
    monkeypatch.setattr(testee.dml, 'get_apofile', mock_load)
    monkeypatch.setattr(testee, 'HERE', testee.pathlib.Path('here'))
    monkeypatch.setattr(testee.Apropos, 'initapp', mock_initapp)
    monkeypatch.setattr(testee.Apropos, 'load_and_set_screenpos', mock_load_and_set)
    monkeypatch.setattr(testee.Apropos, 'page_changed', 'change_page_method')
    monkeypatch.setattr(testee.Apropos, 'closetab', 'close_page_method')
    testobj = testee.Apropos()
    assert isinstance(testobj.gui, testee.gui.AproposGui)
    assert testobj.apofile == 'result from dml.get_apofile(``)'
    assert isinstance(testobj.config, testee.configparser.ConfigParser)
    assert testobj.confpath == testee.pathlib.Path('~/.config/a-propos/locs').expanduser()
    assert capsys.readouterr().out == (
            "called AproposGui with title `A Propos`\n"
            "called AproposGui.set_appicon with arg `here/apropos.ico`\n"
            "called AproposGui.init_trayicon with args ('here/apropos.ico',)"
            " {'tooltip': 'Click to revive Apropos'}\n"
            "called AproposGui.setup_tabwidget with args () {'change_page': 'change_page_method',"
            " 'close_page': 'close_page_method'}\n"
            "called AproposGui.setup_shortcuts\n"
            "called Apropos.load_and_set_screenpos\n"
            "called Apropos.initapp\n")
    testobj = testee.Apropos('filename', 'title')
    assert isinstance(testobj.gui, testee.gui.AproposGui)
    assert testobj.apofile == 'result from dml.get_apofile(`filename`)'
    assert capsys.readouterr().out == (
            "called AproposGui with title `title`\n"
            "called AproposGui.set_appicon with arg `here/apropos.ico`\n"
            "called AproposGui.init_trayicon with args ('here/apropos.ico',)"
            " {'tooltip': 'Click to revive Apropos'}\n"
            "called AproposGui.setup_tabwidget with args () {'change_page': 'change_page_method',"
            " 'close_page': 'close_page_method'}\n"
            "called AproposGui.setup_shortcuts\n"
            "called Apropos.load_and_set_screenpos\n"
            "called Apropos.initapp\n")

def setup_testobj(monkeypatch, capsys):
    """build testobject instance and return itto caller
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    return testobj

def test_apropos_page_changed(monkeypatch, capsys):
    """unittest for main.apropos_page_changed
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.page_changed()
    assert testobj.current == 1
    assert capsys.readouterr().out == ('called AproposGui.get_current_page\n'
                                       'called AproposGui.set_focus_to_page\n')

def test_apropos_quit(monkeypatch, capsys):
    """unittest for main.apropos_quit
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.quit()
    assert capsys.readouterr().out == 'called AproposGui.close\n'

def test_apropos_load_data(monkeypatch, capsys):
    """unittest for main.apropos_load_data
    """
    def mock_initapp(self):
        """stub
        """
        print('called Apropos.initapp')
    def mock_confirm(self, *args):
        """stub
        """
        print('called Apropos.confirm with args', args)
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(testee.Apropos, 'initapp', mock_initapp)
    monkeypatch.setattr(testee.Apropos, 'confirm', mock_confirm)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.load_data()
    assert capsys.readouterr().out == ("called AproposGui.clear_all\n"
                                       "called Apropos.initapp\n"
                                       "called Apropos.confirm with args ('NotifyOnLoad',"
                                       " 'load_text')\n")

def test_apropos_hide_app(monkeypatch, capsys):
    """unittest for main.apropos_hide_app
    """
    def mock_confirm(self, *args):
        """stub
        """
        print('called Apropos.confirm with args', args)
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(testee.Apropos, 'confirm', mock_confirm)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.hide_app()
    assert capsys.readouterr().out == ("called Apropos.confirm with args ('AskBeforeHide',"
                                       " 'hide_text')\n"
                                       "called AproposGui.hide_app\n")

def test_apropos_save_data(monkeypatch, capsys):
    """unittest for main.apropos_save_data
    """
    def mock_afsl(self):
        """stub
        """
        print('called Apropos.afsl')
    def mock_confirm(self, *args):
        """stub
        """
        print('called Apropos.confirm with args', args)
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(testee.Apropos, 'afsl', mock_afsl)
    monkeypatch.setattr(testee.Apropos, 'confirm', mock_confirm)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.save_data()
    assert capsys.readouterr().out == ("called Apropos.afsl\n"
                                       "called Apropos.confirm with args ('NotifyOnSave',"
                                       " 'save_text')\n")

def test_apropos_initapp(monkeypatch, capsys):
    """unittest for main.apropos_initapp
    """
    def mock_load(name):
        """stub
        """
        print('called dml.load_notes with filename `{name}`')
        return {'AskBeforeHide': 'x', 'ActiveTab': 1}, {1: ('x', 'aaa'), 2: ('z', 'bbb')}
    monkeypatch.setattr(testee.dml, 'load_notes', mock_load)
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(testee.Apropos, 'newtab', MockApropos.newtab)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.apofile = 'apofile'
    testobj.initapp()
    assert testobj.opts == {'ActiveTab': 1, 'AskBeforeHide': 'x'}
    assert testobj.apodata == {1: ('x', 'aaa'), 2: ('z', 'bbb')}
    assert testobj.current == 1
    assert capsys.readouterr().out == (
            "called dml.load_notes with filename `{name}`\n"
            "called Apropos.newtab with args {'titel': 'x', 'note': 'aaa'}\n"
            "called Apropos.newtab with args {'titel': 'z', 'note': 'bbb'}\n"
            "called AproposGui.set_current_page with arg `1`\n")
    monkeypatch.setattr(testee.dml, 'load_notes', lambda x: ({'x': 'y'}, {}))
    testobj.initapp()
    assert testobj.opts == {'x': 'y'}
    assert testobj.apodata == {}
    assert testobj.current == 0
    assert capsys.readouterr().out == "called Apropos.newtab with args {}\n"

def test_apropos_newtab(monkeypatch, capsys):
    """unittest for main.apropos_newtab
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.newtab()
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.new_page with args (3, '3', None)\n")
    testobj.newtab('event', 'x')
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.new_page with args (3, 'x', None)\n")
    testobj.newtab('event', 'x', 'y')
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.new_page with args (3, 'x', 'y')\n")

def test_apropos_goto_previous(monkeypatch, capsys):
    """unittest for main.apropos_goto_previous
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.goto_previous()
    assert capsys.readouterr().out == 'called AproposGui.set_previous_page\n'

def test_apropos_goto_next(monkeypatch, capsys):
    """unittest for main.apropos_goto_next
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.goto_next()
    assert capsys.readouterr().out == 'called AproposGui.set_next_page\n'

def test_apropos_closetab(monkeypatch, capsys):
    """unittest for main.apropos_closetab
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(testee.Apropos, 'afsl', MockApropos.afsl)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.current = 1
    testobj.closetab()
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.delete_page with arg `1`\n")
    testobj.closetab('event', 2)
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.delete_page with arg `2`\n")
    monkeypatch.setattr(testobj.gui, 'get_page_count', lambda *x: 1)
    testobj.closetab()
    assert capsys.readouterr().out == ("called AproposGui.clear_last_page\n"
                                       "called Apropos.afsl\n"
                                       "called AproposGui.close\n")

def test_apropos_revive(monkeypatch, capsys):
    """unittest for main.apropos_revive
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.revive()
    assert capsys.readouterr().out == 'called AproposGui.reshow_app with arg `None`\n'
    testobj.revive('event')
    assert capsys.readouterr().out == 'called AproposGui.reshow_app with arg `event`\n'

def test_apropos_afsl(monkeypatch, capsys):
    """unittest for main.apropos_afsl
    """
    def mock_save(*args):
        """stub
        """
        print('called dml.save_notes with args', args)
    def mock_get_and_save(self):
        """stub
        """
        print('called Apropos.get_and_save_screenpos')
    monkeypatch.setattr(testee.Apropos, 'get_and_save_screenpos', mock_get_and_save)
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    monkeypatch.setattr(testee.dml, 'save_notes', mock_save)
    testobj.apofile = 'file'
    testobj.afsl()
    assert testobj.opts["ActiveTab"] == 1
    assert capsys.readouterr().out == ("called AproposGui.get_current_page\n"
                                       "called AproposGui.get_page_count\n"
                                       "called AproposGui.get_page_title with arg `0`\n"
                                       "called AproposGui.get_page_text with arg `0`\n"
                                       "called AproposGui.get_page_title with arg `1`\n"
                                       "called AproposGui.get_page_text with arg `1`\n"
                                       "called dml.save_notes with args ('file', {'ActiveTab': 1},"
                                       " {1: ('page', 'text'), 2: ('page', 'text')})\n"
                                       "called Apropos.get_and_save_screenpos\n")

def test_apropos_helppage(monkeypatch, capsys):
    """unittest for main.apropos_helppage
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    monkeypatch.setattr(testee, 'languages', {'en': {'info': 'info for `en`'}})
    testobj.opts = {'language': 'en'}
    testobj.helppage()
    assert capsys.readouterr().out == 'called AproposGui.meld with arg `info for `en``\n'

def test_apropos_confirm(monkeypatch, capsys):
    """unittest for main.apropos_confirm
    """
    class MockCheck:
        "stub"
        def __init__(self, *args, **kwargs):
            print('called SetCheck with args', args, kwargs)
            self.gui = 'dialog'
    def mock_show(*args):
        print('called AproposGui.show_dialog with args', args)
        return True, False
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.gui.show_dialog = mock_show
    testobj.opts = {'language': 'en', 'setting': 'value'}
    monkeypatch.setattr(testee, 'SetCheck', MockCheck)
    monkeypatch.setattr(testee, 'languages', {'en': {'show_text': 'x', 'textitem': 'y'}})
    testobj.opts['setting'] = True
    testobj.confirm('setting', 'textitem')
    assert testobj.opts['setting']
    # assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('MockCheck',"
    #                                    " {'message': 'y', 'optionvalue': True, 'caption': 'x'})\n")
    assert capsys.readouterr().out == (
            "called SetCheck with args"
            f" ({testobj},) {{'message': 'y', 'optionvalue': False, 'caption': 'x'}}\n"
            "called AproposGui.show_dialog with args ('dialog',)\n")
    testobj.opts['setting'] = False
    testobj.confirm('setting', 'textitem')
    assert capsys.readouterr().out == ''

def test_apropos_asktitle(monkeypatch, capsys):
    """unittest for main.apropos_asktitle
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.current = '1'
    testobj.opts = {'language': 'en'}
    monkeypatch.setattr(testee, 'languages', {'en': {'ask_title': ' x'}})
    testobj.asktitle()
    assert capsys.readouterr().out == (
            "called AproposGui.get_page_title with arg `1`\n"
            "called AproposGui.get_text with args {'prompt': ' x', 'initial': 'page'}\n"
            "called AproposGui.set_page_title with args ('1', 'newtext')\n")
    monkeypatch.setattr(MockAproposGui, 'get_text', lambda *x, **y: ('x', False))
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.current = '1'
    testobj.opts = {'language': 'en'}
    testobj.asktitle()
    assert capsys.readouterr().out == "called AproposGui.get_page_title with arg `1`\n"

def test_apropos_choose_language(monkeypatch, capsys):
    """unittest for main.apropos_choose_language
    """
    monkeypatch.setattr(testee, 'languages', {'x': {'language': 'xxx', 'ask_language': 'xx'},
                                            'y': {'language': 'yyy', 'ask_language': 'yy'}})
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts['language'] = 'y'
    testobj.choose_language()
    assert capsys.readouterr().out == ("called AproposGui.get_item with args {'prompt': 'yy',"
                                       " 'itemlist': ['xxx', 'yyy'], 'initial': 1}\n")
    assert testobj.opts['language'] == 'x'
    monkeypatch.setattr(testee, 'languages', {'x': {'language': 'xxx', 'ask_language': 'xx'},
                                            'y': {'language': 'yyy', 'ask_language': 'yy'}})
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts['language'] = 'y'

    monkeypatch.setattr(MockAproposGui, 'get_item', lambda *x, **y: ('', True))
    testobj.choose_language()
    assert capsys.readouterr().out == ""
    assert testobj.opts['language'] == 'y'

    monkeypatch.setattr(MockAproposGui, 'get_item', lambda *x, **y: ('', False))
    testobj.choose_language()
    assert capsys.readouterr().out == ""
    assert testobj.opts['language'] == 'y'

def test_apropos_options(monkeypatch, capsys):
    """unittest for main.apropos_options
    """
    class MockOptions:
        "stub"
        def __init__(self, *args, **kwargs):
            print('called SetOptions with args', args, kwargs)
            self.gui = 'dialog'
    def mock_show(*args):
        print('called AproposGui.show_dialog with args', args)
        return True, {'AskBeforeHide': ' a', 'NotifyOnLoad': 'b', 'NotifyOnSave': 'c'}
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts = {'language': 'en'}
    monkeypatch.setattr(testee, 'SetOptions', MockOptions)
    monkeypatch.setattr(testee, 'languages', {'en': {'ask_hide': ' x', 'notify_load': 'y',
                                                   'notify_save': 'z'}})
    testobj.options()
    assert testobj.opts == {'language': 'en'}
    # assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('MockOptions',"
    #                                    " {'text2valuedict': {'AskBeforeHide': ' x',"
    #                                    " 'NotifyOnLoad': 'y', 'NotifyOnSave': 'z'}})\n")
    assert capsys.readouterr().out == (
            f"called SetOptions with args ({testobj},"
            " {'AskBeforeHide': ' x', 'NotifyOnLoad': 'y', 'NotifyOnSave': 'z'}) {}\n"
            "called AproposGui.show_dialog with args ('dialog',)\n")
    testobj.gui.show_dialog = mock_show
    testobj.options()
    assert testobj.opts == {'language': 'en', 'AskBeforeHide': ' a', 'NotifyOnLoad': 'b',
                            'NotifyOnSave': 'c'}
    # assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('MockOptions',"
    #                                    " {'text2valuedict': {'AskBeforeHide': ' x',"
    #                                    " 'NotifyOnLoad': 'y', 'NotifyOnSave': 'z'}})\n")
    assert capsys.readouterr().out == (
            f"called SetOptions with args ({testobj},"
            " {'AskBeforeHide': ' x', 'NotifyOnLoad': 'y', 'NotifyOnSave': 'z'}) {}\n"
            "called AproposGui.show_dialog with args ('dialog',)\n")

def test_set_config_values_from_screen(monkeypatch, capsys):
    """unittest for main.set_config_values_from_screen
    """
    def mock_get():
        print('called AproposGui.get_screen_dimensions')
        return 'xxy', 'wxh'
    testobj = setup_testobj(monkeypatch, capsys)
    testobj.config = testee.configparser.ConfigParser()
    testobj.gui.get_screen_dimensions = mock_get
    testobj.apofile = testee.pathlib.Path('qqq')
    testobj_apofile = str(testobj.apofile.resolve())
    testobj.config.add_section(testobj_apofile)
    testobj.config[testobj_apofile]['pos'] = ''
    testobj.config[testobj_apofile]['size'] = ''
    testobj.set_config_values_from_screen()
    assert testobj.config[testobj_apofile]['pos'] == 'xxy'
    assert testobj.config[testobj_apofile]['size'] == 'wxh'
    assert capsys.readouterr().out == 'called AproposGui.get_screen_dimensions\n'

def test_load_and_set_screenpos(monkeypatch, capsys, tmp_path):
    """unittest for main.load_and_set_screenpos
    """
    def mock_set(*args):
        print('called AproposGui.set_screen_dimensions with args', args)
    def mock_set_from(*args):
        print('called Apropos.set_config_values_from_screen')
    confpath = tmp_path / 'testloadconf'
    testobj = setup_testobj(monkeypatch, capsys)
    testobj.config = testee.configparser.ConfigParser()
    testobj.gui.set_screen_dimensions = mock_set
    testobj.set_config_values_from_screen = mock_set_from
    # testobj.apofile = 'qqq'
    testobj.apofile = testee.pathlib.Path('qqq')
    testobj_apofile = str(testobj.apofile.resolve())
    testobj.confpath = confpath
    testobj.load_and_set_screenpos()
    assert testobj.config.has_section(testobj_apofile)
    assert testobj.config.items(testobj_apofile) == []
    assert capsys.readouterr().out == "called Apropos.set_config_values_from_screen\n"
    testobj.config = testee.configparser.ConfigParser()
    confpath.write_text('')
    testobj.load_and_set_screenpos()
    assert testobj.config.has_section(testobj_apofile)
    assert testobj.config.items(testobj_apofile) == []
    assert capsys.readouterr().out == "called Apropos.set_config_values_from_screen\n"
    testobj.config = testee.configparser.ConfigParser()
    confpath.write_text(f'[{testobj_apofile}]\npos=yyy\nsize=zzz\n')
    testobj.load_and_set_screenpos()
    assert testobj.config.has_section(testobj_apofile)
    assert testobj.config.items(testobj_apofile) == [('pos', 'yyy'), ('size', 'zzz')]
    assert capsys.readouterr().out == (
            "called AproposGui.set_screen_dimensions with args ('yyy', 'zzz')\n")

def test_get_and_save_screenpos(monkeypatch, capsys, tmp_path):
    """unittest for main.get_and_save_screenpos
    """
    def mock_set_from(*args):
        print('called Apropos.set_config_values_from_screen')
    confpath = tmp_path / 'testsaveconf'
    testobj = setup_testobj(monkeypatch, capsys)
    testobj.config = testee.configparser.ConfigParser()
    testobj.set_config_values_from_screen = mock_set_from
    testobj.apofile = 'qqq'
    testobj.confpath = confpath
    testobj.get_and_save_screenpos()
    assert confpath.exists()
    assert capsys.readouterr().out == "called Apropos.set_config_values_from_screen\n"


class TestSetOptions:
    """Unittests for main.SetOptions
    """
    def test_init(self, monkeypatch, capsys):
        """Unittest for SetOptions.__init__
        """
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called OptionsDialog.__init__ with args', args, kwargs)
            def add_checkbox_line_to_grid(self, *args):
                print('called OptionsDialog.add_checkbox_line_to_grid with args', args)
                return 'check'
            def add_buttonbox(self, **kwargs):
                print('called OptionsDialog.add_buttonbox with args', kwargs)
        monkeypatch.setattr(testee.gui, 'OptionsDialog', MockDialog)
        parent = types.SimpleNamespace(opts={'x': 'a', 'y': 'b'}, gui='mainwindow')
        testobj = testee.SetOptions(parent, {'x': 'xxxx', 'y': 'yyyy'})
        assert testobj.parent == parent
        assert not testobj.dialog_data
        assert testobj.controls == [('x', 'check'), ('y', 'check')]
        assert isinstance(testobj.gui, testee.gui.OptionsDialog)
        assert capsys.readouterr().out == (
                f"called OptionsDialog.__init__ with args ({testobj}, '{parent.gui}') {{}}\n"
                "called OptionsDialog.add_checkbox_line_to_grid with args (1, 'xxxx', 'a')\n"
                "called OptionsDialog.add_checkbox_line_to_grid with args (2, 'yyyy', 'b')\n"
                "called OptionsDialog.add_buttonbox with args"
                " {'okvalue': '&Apply', 'cancelvalue': '&Close'}\n")

    def test_confirm(self, monkeypatch, capsys):
        """Unittest for SetOptions.confirm
        """
        def mock_init(self, *args):
            print('called SetOptions.__init__ with args', args)
        def mock_get(*args):
            print('called OptionsDialog.get_checkbox_value with args', args)
            return 'value'
        parent = 'parent'
        monkeypatch.setattr(testee.SetOptions, '__init__', mock_init)
        testobj = testee.SetOptions(parent, 'title', {'x': 'xxxx', 'y': 'yyyy'})
        testobj.controls = [('x', 'checkbox'), ('y', 'checkbox2')]
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get)
        assert testobj.confirm() == {'x': 'value', 'y': 'value'}
        assert capsys.readouterr().out == (
                "called SetOptions.__init__ with args"
                " ('parent', 'title', {'x': 'xxxx', 'y': 'yyyy'})\n"
                "called OptionsDialog.get_checkbox_value with args ('checkbox',)\n"
                "called OptionsDialog.get_checkbox_value with args ('checkbox2',)\n")


class TestSetCheck:
    """Unittests for main.SetCheck
    """
    def test_init(self, monkeypatch, capsys):
        """Unittest for SetCheck.__init__
        """
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called OptionsDialog.__init__ with args', args, kwargs)
            def add_label(self, message):
                print(f"called OptionsDialog.add_label with arg '{message}'")
            def add_checkbox(self, *args):
                print('called OptionsDialog.add_checkbox with args', args)
                return 'check'
            def add_ok_buttonbox(self):
                print('called OptionsDialog.add_ok_buttonbox')
        monkeypatch.setattr(testee.gui, 'CheckDialog', MockDialog)
        parent = MockApropos()
        assert capsys.readouterr().out == ("called Apropos with args {}\n"
                                           "called AproposGui with title `title`\n")
        testobj = testee.SetCheck(parent, 'x', 'y', 'z')
        assert testobj.parent == parent
        assert not testobj.dialog_data
        assert isinstance(testobj.gui, testee.gui.CheckDialog)
        assert testobj.check == 'check'
        assert capsys.readouterr().out == (
                f"called OptionsDialog.__init__ with args ({testobj}, {parent.gui}) {{}}\n"
                "called OptionsDialog.add_label with arg 'x'\n"
                "called OptionsDialog.add_checkbox with args ('z', 'y')\n"
                "called OptionsDialog.add_ok_buttonbox\n")

    def test_confirm(self, monkeypatch, capsys):
        """Unittest for SetCheck.confirm
        """
        def mock_init(self, *args):
            print('called CheckDialog.__init__ with args', args)
        def mock_get(*args):
            print('called CheckDialog.get_checkbox_value with args', args)
            return 'value'
        monkeypatch.setattr(testee.SetCheck, '__init__', mock_init)
        parent = 'parent'
        testobj = testee.SetCheck(parent, 'title', 'x', 'y', 'z')
        assert capsys.readouterr().out == (
                "called CheckDialog.__init__ with args ('parent', 'title', 'x', 'y', 'z')\n")
        testobj.check = 'checkbox'
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get)
        assert testobj.confirm() == 'value'
        assert capsys.readouterr().out == (
                "called CheckDialog.get_checkbox_value with args ('checkbox',)\n")
