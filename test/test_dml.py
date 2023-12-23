from apropos import dml

def test_get_apofile(monkeypatch, capsys):
    assert dml.get_apofile('') == dml.pathlib.Path('apropos.apo')
    assert dml.get_apofile('test') == dml.pathlib.Path('test.apo')
    assert dml.get_apofile('testing.pck') == dml.pathlib.Path('testing.apo')


def test_load_notes_file_not_found(tmp_path):
    """run the load_notes method with no existing file
    """
    # monkeypatch.setattr(dml.pathlib.Path, 'exists', lambda *x: False)
    apofile = tmp_path / 'apropos.apo'
    opts, apodata = dml.load_notes(apofile)
    assert opts == {"AskBeforeHide": True, "ActiveTab": 0, 'language': 'eng',
                    'NotifyOnSave': True, 'NotifyOnLoad': True}
    assert apodata == {}

def test_load_notes_not_a_pickle(tmp_path):
    """run the load_notes method with a non-pickle file
    """
    apofile = tmp_path / 'apropos.apo'
    with apofile.open(mode='w') as f:
        f.write("oihgyavjjvjdvj  diidn dnni")
        f.write("\n")
    opts, apodata = dml.load_notes(apofile)

def test_load_notes_happy_flow(tmp_path):
    """run the load_notes method on a "correct" file
    """
    apofile = tmp_path / 'apropos.apo'
    with apofile.open(mode='wb') as f:
        dml.pickle.dump({0: 'opts', 1: 'apodata'}, f, protocol=2)
    opts, apodata = dml.load_notes(apofile)
    assert opts == 'opts'
    assert apodata == {1: 'apodata'}

def test_save_notes_happy_flow(tmp_path):
    """save the notes and check if it's readable correctly
    """
    apofile = tmp_path / 'apropos.apo'
    opts = 'opts'
    apodata = {1: 'apodata'}
    dml.save_notes(apofile, opts, apodata)
    with apofile.open(mode='rb') as f:
        data = dml.pickle.load(f)
    assert data == {0: 'opts', 1: 'apodata'}
