"""apomixin.py

gui-independent part of my apropos application
(mostly I/O functions)
"""

import pathlib
import sys
import pickle
if sys.version >= '3':
    from apropos import en, nl
else:
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
            apodata = {}
        else:
            try:
                with self.apofile.open(mode='rb') as f_in:
                    apodata = pickle.load(f_in)
            except ValueError:
                with self.apofile.open(mode='r') as f_in:
                    apodata = pickle.load(f_in)
        return apodata

    def save_notes(self, data):
        """(re)save data file
        """
        with self.apofile.open(mode='wb') as f_out:
            pickle.dump(data, f_out, protocol=2)
