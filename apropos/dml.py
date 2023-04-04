"""apropos data management routines
"""

import pathlib
import pickle


def get_apofile(name):
    """convert name of data file to a path

    use standard name if empty
    """
    return pathlib.Path(name or 'apropos').with_suffix('.apo')


def load_notes(apofile):
    """load or initialize data file

    expects a pathlib.Path; returns options and notes data separately
    """
    if not apofile.exists():
        opts = {"AskBeforeHide": True, "ActiveTab": 0, 'language': 'eng',
                'NotifyOnSave': True, 'NotifyOnLoad': True}
        apodata = {}
    else:
        try:
            with apofile.open(mode='rb') as f_in:
                apodata = pickle.load(f_in)
        except pickle.UnpicklingError:
            opts, apodata = {}, {}
        else:
            opts = apodata.pop(0)  # zie save_notes: hoort altijd aanwezig te zijn
    return opts, apodata


def save_notes(apofile, opts, data):
    """(re)save data file
    """
    data[0] = opts
    with apofile.open(mode='wb') as f_out:
        pickle.dump(data, f_out, protocol=2)
