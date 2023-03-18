import types
import pytest

from apropos import main

class MockApropos:
    def __init__(self, **kwargs):
        print('called Apropos with args', kwargs)
        self.gui = MockAproposGui()

class MockAproposGui:
    def __init__(self, **kwargs):
        print('called AproposGui')
    def go(self):
        print('called AproposGui.go')

def test_apropos(monkeypatch, capsys):
    monkeypatch.setattr(main, 'Apropos', MockApropos)
    main.apropos()
    assert capsys.readouterr().out == ("called Apropos with args {'fname': '', 'title': ''}\n"
                                       'called AproposGui\n'
                                       'called AproposGui.go\n')
    main.apropos(fname='x', title='y')
    assert capsys.readouterr().out == ("called Apropos with args {'fname': 'x', 'title': 'y'}\n"
                                       'called AproposGui\n'
                                       'called AproposGui.go\n')
