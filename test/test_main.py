"""unittests for ./apropos/main.py
"""
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
    def mock_load_and_set(fname):
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
    def mock_get_and_save(fname):
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
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts = {'language': 'en', 'setting': 'value'}
    monkeypatch.setattr(testee.gui, 'CheckDialog', 'checkdialog')
    monkeypatch.setattr(testee, 'languages', {'en': {'show_text': 'x', 'textitem': 'y'}})
    testobj.opts['setting'] = True
    testobj.confirm('setting', 'textitem')
    assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('checkdialog',"
                                       " {'message': 'y', 'option': 'setting', 'caption': 'x'})\n")
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
    monkeypatch.setattr(MockAproposGui, 'get_item', lambda *x, **y: ('', False))
    testobj.choose_language()
    assert capsys.readouterr().out == ""
    assert testobj.opts['language'] == 'y'

def test_apropos_options(monkeypatch, capsys):
    """unittest for main.apropos_options
    """
    monkeypatch.setattr(testee.Apropos, '__init__', MockApropos.__init__)
    testobj = testee.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts = {'language': 'en'}
    monkeypatch.setattr(testee.gui, 'OptionsDialog', 'optionsdialog')
    monkeypatch.setattr(testee, 'languages', {'en': {'ask_hide': ' x', 'notify_load': 'y',
                                                   'notify_save': 'z'}})
    testobj.options()
    assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('optionsdialog',"
                                       " {'sett2text': {'AskBeforeHide': ' x', 'NotifyOnLoad': 'y',"
                                       " 'NotifyOnSave': 'z'}})\n")

def test_set_config_values_from_screen(monkeypatch, capsys):
    def mock_get():
        print('called AproposGui.get_screen_dimensions')
        return 'xxy', 'wxh'
    testobj = setup_testobj(monkeypatch, capsys)
    testobj.config = testee.configparser.ConfigParser()
    testobj.gui.get_screen_dimensions = mock_get
    testobj.apofile = 'qqq'
    testobj.config.add_section(testobj.apofile)
    testobj.config[testobj.apofile]['pos'] = ''
    testobj.config[testobj.apofile]['size'] = ''
    testobj.set_config_values_from_screen()
    assert testobj.config[testobj.apofile]['pos'] == 'xxy'
    assert testobj.config[testobj.apofile]['size'] == 'wxh'
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
    testobj.apofile = 'qqq'
    testobj.confpath = confpath
    testobj.load_and_set_screenpos()
    assert testobj.config.has_section('qqq')
    assert testobj.config.items('qqq') == []
    assert capsys.readouterr().out == "called Apropos.set_config_values_from_screen\n"
    testobj.config = testee.configparser.ConfigParser()
    confpath.write_text('')
    testobj.load_and_set_screenpos()
    assert testobj.config.has_section('qqq')
    assert testobj.config.items('qqq') == []
    assert capsys.readouterr().out == "called Apropos.set_config_values_from_screen\n"
    testobj.config = testee.configparser.ConfigParser()
    confpath.write_text('[qqq]\npos=yyy\nsize=zzz\n')
    testobj.load_and_set_screenpos()
    assert testobj.config.has_section('qqq')
    assert testobj.config.items('qqq') == [('pos', 'yyy'), ('size', 'zzz')]
    assert capsys.readouterr().out == (
            "called AproposGui.set_screen_dimensions with args ('yyy', 'zzz')\n")

def test_get_and_save_screenpos(monkeypatch, capsys, tmp_path):
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
