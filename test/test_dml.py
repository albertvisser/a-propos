"""unittests for ./apropos/dml.py
"""
from apropos import dml as testee


def test_get_apofile():
    """unittest for dml.get_apofile
    """
    assert testee.get_apofile('') == testee.pathlib.Path('apropos.apo')
    assert testee.get_apofile('test') == testee.pathlib.Path('test.apo')
    assert testee.get_apofile('testing.pck') == testee.pathlib.Path('testing.apo')


def test_load_notes_file_not_found(tmp_path):
    """unittest for dml.load_notes: no existing file
    """
    # monkeypatch.setattr(dml.pathlib.Path, 'exists', lambda *x: False)
    apofile = tmp_path / 'apropos.apo'
    opts, apodata = testee.load_notes(apofile)
    assert opts == {"AskBeforeHide": True, "ActiveTab": 0, 'language': 'eng',
                    'NotifyOnSave': True, 'NotifyOnLoad': True}
    assert apodata == {}


def test_load_notes_not_a_pickle(tmp_path):
    """unittest for dml.load_notes: non-pickle file
    """
    apofile = tmp_path / 'apropos.apo'
    with apofile.open(mode='w') as f:
        f.write("oihgyavjjvjdvj  diidn dnni")
        f.write("\n")
    opts, apodata = testee.load_notes(apofile)
    # assert apodata == {}


def test_load_notes_happy_flow(tmp_path):
    """unittest for dml.load_notes: usable file
    """
    apofile = tmp_path / 'apropos.apo'
    with apofile.open(mode='wb') as f:
        testee.pickle.dump({0: 'opts', 1: 'apodata'}, f, protocol=2)
    opts, apodata = testee.load_notes(apofile)
    assert opts == 'opts'
    assert apodata == {1: 'apodata'}


def test_save_notes_happy_flow(tmp_path):
    """save the notes and check if it's readable correctly
    """
    apofile = tmp_path / 'apropos.apo'
    opts = 'opts'
    apodata = {1: 'apodata'}
    testee.save_notes(apofile, opts, apodata)
    with apofile.open(mode='rb') as f:
        data = testee.pickle.load(f)
    assert data == {0: 'opts', 1: 'apodata'}
