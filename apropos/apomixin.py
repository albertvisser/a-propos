"""apomixin.py

gui-independent part of my apropos application
(mostly I/O functions)
"""

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
import sys
import pickle
## import pdb
try:    # if sys.version >= '3':
    from apropos import en, nl
except ImportError: # else:
    import en, nl

languages = {}
languages.update(en.lang)
languages.update(nl.lang)


class ApoMixin(object):
    """Mixin class containing generally usable methods
    """

    def set_apofile(self, name):
        """determine name of data file
        """
        if name:
            self.apofile = pathlib.Path(name)
        else:
            self.apofile = pathlib.Path("apropos.pck")

    def load_notes(self):
        """load or initialize data file
        """
        if not self.apofile.exists():
            self.apodata = {}
        else:
            try:
                with self.apofile.open(mode='rb') as f_in:
                    self.apodata = pickle.load(f_in)
            except ValueError:
                with self.apofile.open(mode='r') as f_in:
                    self.apodata = pickle.load(f_in)

    def save_notes(self, data):
        """(re)save data file
        """
        with self.apofile.open(mode='wb') as f_out:
            pickle.dump(data, f_out, protocol=2)
