"""apomixin.py

gui-independent part of my apropos application
(logging setup, language support, I/O functions)
"""

import pathlib
import os
import pickle
import logging
## import pdb
import apropos.en as en
import apropos.nl as nl

languages = {}
languages.update(en.lang)
languages.update(nl.lang)

HERE = pathlib.Path(__file__).parent  # os.path.dirname(__file__)
iconame = str(HERE / "apropos.ico")
LOGFILE = HERE.parent / 'logs' / 'apropos_qt.log'
WANT_LOGGING = 'DEBUG' in os.environ and os.environ["DEBUG"] != "0"
if WANT_LOGGING:
    LOGFILE.parent.mkdir(exist_ok=True)
    LOGFILE.touch(exist_ok=True)
    logging.basicConfig(filename=str(LOGFILE),
                        level=logging.DEBUG, format='%(asctime)s %(message)s')


def log(message, always=False):
    "only log when DEBUG is set in environment"
    if WANT_LOGGING or always:
        logging.info(message)


def get_setttexts(settdict):
    """returns the texts associated with the message dialogs that can be hidden
    """
    return {'AskBeforeHide': languages[settdict["language"]]['ask_hide'],
            'NotifyOnLoad': languages[settdict["language"]]['notify_load'],
            'NotifyOnSave': languages[settdict["language"]]['notify_save']}


def get_shortcuts():
    """return a list of actions and associated keyboard shortcuts

    Because of how the application is constructed, the callbacks cannot be defined here but have
    to be associated in the gui modules.
    """
    return (('reload', ('Ctrl+R',)),
            ('newtab', ('Ctrl+N',)),
            ('close', ('Ctrl+W',)),
            ('hide', ('Ctrl+H',)),
            ('save', ('Ctrl+S',)),
            ('quit', ('Ctrl+Q', 'Escape')),
            ('language', ('Ctrl+L',)),
            ('next', ('Alt+Right',)),
            ('prev', ('Alt+Left',)),
            ('help', ('F1',)),
            ('title', ('F2',)),
            ('settings', ('Alt+P',)))


def get_apofile(name):
    """convert name of data file to a path

    use standard name if empty
    """
    return pathlib.Path(name or 'apropos').with_suffix('.apo')


def load_notes(apofile):
    """load or initialize data file
    """
    if not apofile.exists():
        opts = {"AskBeforeHide": True, "ActiveTab": 0, 'language': 'eng',
                'NotifyOnSave': True, 'NotifyOnLoad': True}
        apodata = {}
    else:
        try:
            with apofile.open(mode='rb') as f_in:
                apodata = pickle.load(f_in)
        except ValueError:
            with apofile.open(mode='r') as f_in:
                apodata = pickle.load(f_in)
        if 0 in apodata:
            opts = apodata.pop(0)
    return opts, apodata


def save_notes(apofile, data):
    """(re)save data file
    """
    with apofile.open(mode='wb') as f_out:
        pickle.dump(data, f_out, protocol=2)
