# -*- coding: utf-8 -*-

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

    def set_apofile(self, name):
        if name:
            self.apofile = pathlib.Path(name)
        else:
            self.apofile = pathlib.Path("apropos.pck")

    def load_notes(self):
        if not self.apofile.exists():
            self.apodata = {}
            return
        try:
            with self.apofile.open(mode='rb') as f:
                self.apodata = pickle.load(f)
        except ValueError:
            with self.apofile.open(mode='r') as f:
                self.apodata = pickle.load(f)

    def save_notes(self):
        with self.apofile.open(mode='wb') as f:
            pickle.dump(self.apodata, f, protocol=2)
