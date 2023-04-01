import types
import pytest

from apropos import main

class MockApropos:
    def __init__(self, **kwargs):
        print('called Apropos with args', kwargs)
        self.gui = MockAproposGui(self, 'title')
        self.opts = {}
    def newtab(self, **kwargs):
        print('called Apropos.newtab with args', kwargs)
    def afsl(self):
        print('called Apropos.afsl')

class MockAproposGui:
    def __init__(self, master, title):
        self.master = master
        print(f'called AproposGui with title `{title}`')
    def go(self):
        print('called AproposGui.go')
    def close(self):
        print('called AproposGui.close')
    def set_appicon(self, name):
        print(f'called AproposGui.set_appicon with arg `{name}`')
    def init_trayicon(self, *args, **kwargs):
        print('called AproposGui.init_trayicon with args', args, kwargs)
    def setup_tabwidget(self, *args, **kwargs):
        print('called AproposGui.setup_tabwidget with args', args, kwargs)
    def setup_shortcuts(self, menudict):
        # print(f'called AproposGui.setup_shortcuts with arg `{menudict}`')
        # geen argument laten zien spaart een hoop simulatie-opzetten uit
        print('called AproposGui.setup_shortcuts')
    def get_current_page(self):
        print('called AproposGui.get_current_page')
        return 1
    def set_focus_to_page(self):
        print('called AproposGui.set_focus_to_page')
    def clear_last_page(self):
        print('called AproposGui.clear_last_page')
    def clear_all(self):
        print('called AproposGui.clear_all')
    def hide_app(self):
        print('called AproposGui.hide_app')
    def set_current_page(self, pageno=None):
        if pageno is None:
            print(f'called AproposGui.set_current_page')
        else:
            print(f'called AproposGui.set_current_page with arg `{pageno}`')
    def set_previous_page(self):
        print('called AproposGui.set_previous_page')
    def set_next_page(self):
        print('called AproposGui.set_next_page')
    def get_page_count(self):
        print('called AproposGui.get_page_count')
        return 2
    def new_page(self, *args):
        print('called AproposGui.new_page with args', args)
    def reshow_app(self, name):
        print(f'called AproposGui.reshow_app with arg `{name}`')
    def meld(self, msg):
        print(f'called AproposGui.meld with arg `{msg}`')
    def show_dialog(self, *args):
        print(f'called AproposGui.show_dialog with args', args)
    def get_text(self, **kwargs):
        print('called AproposGui.get_text with args', kwargs)
        return 'newtext', True
    def get_item(self, **kwargs):
        print('called AproposGui.get_item with args', kwargs)
        return 'xxx', True
    def get_page_text(self, pagenum):
        print(f'called AproposGui.get_page_text with arg `{pagenum}`')
        return 'text'
    def get_page_title(self, pagenum):
        print(f'called AproposGui.get_page_title with arg `{pagenum}`')
        return 'page'
    def set_page_title(self, *args):
        print('called AproposGui.set_page_title with args', args)
    def delete_page(self, pagenum):
        print(f'called AproposGui.delete_page with arg `{pagenum}`')


def test_apropos(monkeypatch, capsys):
    monkeypatch.setattr(main, 'Apropos', MockApropos)
    main.apropos()
    assert capsys.readouterr().out == ("called Apropos with args {'fname': '', 'title': ''}\n"
                                       'called AproposGui with title `title`\n'
                                       'called AproposGui.go\n')
    main.apropos(fname='x', title='y')
    assert capsys.readouterr().out == ("called Apropos with args {'fname': 'x', 'title': 'y'}\n"
                                       'called AproposGui with title `title`\n'
                                       'called AproposGui.go\n')

def test_apropos_init(monkeypatch, capsys):
    def mock_load(fname):
        return (f'result from dml.get_apofile(`{fname}`)')
    def mock_initapp(self):
        print('called Apropos.initapp')
    monkeypatch.setattr(main.gui, 'AproposGui', MockAproposGui)
    monkeypatch.setattr(main.dml, 'get_apofile', mock_load)
    monkeypatch.setattr(main, 'HERE', main.pathlib.Path('here'))
    monkeypatch.setattr(main.Apropos, 'initapp', mock_initapp)
    monkeypatch.setattr(main.Apropos, 'page_changed', 'change_page_method')
    monkeypatch.setattr(main.Apropos, 'closetab', 'close_page_method')
    testobj = main.Apropos()
    assert isinstance(testobj.gui, main.gui.AproposGui)
    assert testobj.apofile == 'result from dml.get_apofile(``)'
    assert capsys.readouterr().out == (
            "called AproposGui with title `A Propos`\n"
            "called AproposGui.set_appicon with arg `here/apropos.ico`\n"
            "called AproposGui.init_trayicon with args ('here/apropos.ico',)"
            " {'tooltip': 'Click to revive Apropos'}\n"
            "called AproposGui.setup_tabwidget with args () {'change_page': 'change_page_method',"
            " 'close_page': 'close_page_method'}\n"
            "called AproposGui.setup_shortcuts\n"
            "called Apropos.initapp\n")
    testobj = main.Apropos('filename', 'title')
    assert isinstance(testobj.gui, main.gui.AproposGui)
    assert testobj.apofile == 'result from dml.get_apofile(`filename`)'
    assert capsys.readouterr().out == (
            "called AproposGui with title `title`\n"
            "called AproposGui.set_appicon with arg `here/apropos.ico`\n"
            "called AproposGui.init_trayicon with args ('here/apropos.ico',)"
            " {'tooltip': 'Click to revive Apropos'}\n"
            "called AproposGui.setup_tabwidget with args () {'change_page': 'change_page_method',"
            " 'close_page': 'close_page_method'}\n"
            "called AproposGui.setup_shortcuts\n"
            "called Apropos.initapp\n")

def test_page_changed(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.page_changed()
    assert testobj.current == 1
    assert capsys.readouterr().out == ('called AproposGui.get_current_page\n'
                                       'called AproposGui.set_focus_to_page\n')

def test_load_data(monkeypatch, capsys):
    def mock_initapp(self):
        print('called Apropos.initapp')
    def mock_confirm(self, *args):
        print('called Apropos.confirm with args', args)
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(main.Apropos, 'initapp', mock_initapp)
    monkeypatch.setattr(main.Apropos, 'confirm', mock_confirm)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.load_data()
    assert capsys.readouterr().out == ("called AproposGui.clear_all\n"
                                       "called Apropos.initapp\n"
                                       "called Apropos.confirm with args ('NotifyOnLoad',"
                                       " 'load_text')\n")

def test_hide_app(monkeypatch, capsys):
    def mock_confirm(self, *args):
        print('called Apropos.confirm with args', args)
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(main.Apropos, 'confirm', mock_confirm)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.hide_app()
    assert capsys.readouterr().out == ("called Apropos.confirm with args ('AskBeforeHide',"
                                       " 'hide_text')\n"
                                       "called AproposGui.hide_app\n")

def test_save_data(monkeypatch, capsys):
    def mock_afsl(self):
        print('called Apropos.afsl')
    def mock_confirm(self, *args):
        print('called Apropos.confirm with args', args)
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(main.Apropos, 'afsl', mock_afsl)
    monkeypatch.setattr(main.Apropos, 'confirm', mock_confirm)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.save_data()
    assert capsys.readouterr().out == ("called Apropos.afsl\n"
                                       "called Apropos.confirm with args ('NotifyOnSave',"
                                       " 'save_text')\n")

def test_initapp(monkeypatch, capsys):
    def mock_load(name):
        print('called dml.load_notes with filename `{name}`')
        return {'AskBeforeHide': 'x', 'ActiveTab': 1}, {1: ('x', 'aaa'), 2: ('z', 'bbb')}
    monkeypatch.setattr(main.dml, 'load_notes', mock_load)
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(main.Apropos, 'newtab', MockApropos.newtab)
    testobj = main.Apropos()
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
    monkeypatch.setattr(main.dml, 'load_notes', lambda x: ({'x': 'y'}, {}))
    testobj.initapp()
    assert testobj.opts == {'x': 'y'}
    assert testobj.apodata == {}
    assert testobj.current == 0
    assert capsys.readouterr().out == "called Apropos.newtab with args {}\n"

def test_newtab(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.newtab()
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.new_page with args (3, '3', None)\n")
    testobj.newtab('x')
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.new_page with args (3, 'x', None)\n")
    testobj.newtab('x', 'y')
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.new_page with args (3, 'x', 'y')\n")

def test_goto_previous(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.goto_previous()
    assert capsys.readouterr().out == 'called AproposGui.set_previous_page\n'

def test_goto_next(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.goto_next()
    assert capsys.readouterr().out == 'called AproposGui.set_next_page\n'

def test_closetab(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    monkeypatch.setattr(main.Apropos, 'afsl', MockApropos.afsl)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.current = 1
    testobj.closetab()
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.delete_page with arg `1`\n")
    testobj.closetab(2)
    assert capsys.readouterr().out == ("called AproposGui.get_page_count\n"
                                       "called AproposGui.delete_page with arg `2`\n")
    monkeypatch.setattr(testobj.gui, 'get_page_count', lambda *x: 1)
    testobj.closetab()
    assert capsys.readouterr().out == ("called AproposGui.clear_last_page\n"
                                       "called Apropos.afsl\n"
                                       "called AproposGui.close\n")

def test_revive(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.revive()
    assert capsys.readouterr().out == 'called AproposGui.reshow_app with arg `None`\n'
    testobj.revive('event')
    assert capsys.readouterr().out == 'called AproposGui.reshow_app with arg `event`\n'

def test_afsl(monkeypatch, capsys):
    def mock_save(*args):
        print('called dml.save_notes with args', args)
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    monkeypatch.setattr(main.dml, 'save_notes', mock_save)
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
                                       " {1: ('page', 'text'), 2: ('page', 'text')})\n")

def test_helppage(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    monkeypatch.setattr(main, 'languages', {'en': {'info': 'info for `en`'}})
    testobj.opts = {'language': 'en'}
    testobj.helppage()
    assert capsys.readouterr().out == 'called AproposGui.meld with arg `info for `en``\n'

def test_confirm(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts = {'language': 'en', 'setting': 'value'}
    monkeypatch.setattr(main.gui, 'CheckDialog', 'checkdialog')
    monkeypatch.setattr(main, 'languages', {'en': {'show_text': 'x', 'textitem': 'y'}})
    testobj.opts['setting'] = True
    testobj.confirm('setting', 'textitem')
    assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('checkdialog',"
                                       " {'message': 'y', 'option': 'setting', 'caption': 'x'})\n")
    testobj.opts['setting'] = False
    testobj.confirm('setting', 'textitem')
    assert capsys.readouterr().out == ''

def test_asktitle(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.current = '1'
    testobj.opts = {'language': 'en'}
    monkeypatch.setattr(main, 'languages', {'en': {'ask_title':' x'}})
    testobj.asktitle()
    assert capsys.readouterr().out == (
            "called AproposGui.get_page_title with arg `1`\n"
            "called AproposGui.get_text with args {'prompt': ' x', 'initial': 'page'}\n"
            "called AproposGui.set_page_title with args ('1', 'newtext')\n")
    monkeypatch.setattr(MockAproposGui, 'get_text', lambda *x, **y: ('x', False))
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.current = '1'
    testobj.opts = {'language': 'en'}
    testobj.asktitle()
    assert capsys.readouterr().out == "called AproposGui.get_page_title with arg `1`\n"

def test_choose_language(monkeypatch, capsys):
    monkeypatch.setattr(main, 'languages', {'x': {'language': 'xxx', 'ask_language': 'xx'},
                                            'y': {'language': 'yyy', 'ask_language': 'yy'}})
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts['language'] = 'y'
    testobj.choose_language()
    assert capsys.readouterr().out == ("called AproposGui.get_item with args {'prompt': 'yy',"
                                       " 'itemlist': ['xxx', 'yyy'], 'initial': 1}\n")
    assert testobj.opts['language'] == 'x'
    monkeypatch.setattr(main, 'languages', {'x': {'language': 'xxx', 'ask_language': 'xx'},
                                            'y': {'language': 'yyy', 'ask_language': 'yy'}})
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts['language'] = 'y'
    monkeypatch.setattr(MockAproposGui, 'get_item', lambda *x, **y: ('', False))
    testobj.choose_language()
    assert capsys.readouterr().out == ""
    assert testobj.opts['language'] == 'y'

def test_options(monkeypatch, capsys):
    monkeypatch.setattr(main.Apropos, '__init__', MockApropos.__init__)
    testobj = main.Apropos()
    assert capsys.readouterr().out == ('called Apropos with args {}\n'
                                       'called AproposGui with title `title`\n')
    testobj.opts = {'language': 'en'}
    monkeypatch.setattr(main.gui, 'OptionsDialog', 'optionsdialog')
    monkeypatch.setattr(main, 'languages', {'en': {'ask_hide':' x', 'notify_load': 'y',
                                                   'notify_save': 'z'}})
    testobj.options()
    assert capsys.readouterr().out == ("called AproposGui.show_dialog with args ('optionsdialog',"
                                       " {'sett2text': {'AskBeforeHide': ' x', 'NotifyOnLoad': 'y',"
                                       " 'NotifyOnSave': 'z'}})\n")
