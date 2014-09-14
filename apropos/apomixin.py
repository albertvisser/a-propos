# -*- coding: utf-8 -*-

import pathlib
import sys
import pickle
if sys.version >= '3':
    from apropos import en, nl
else:
    import en, nl
apofile = pathlib.Path("apropos.pck")

languages = {}
languages.update(en.lang)
languages.update(nl.lang)

class ApoMixin(object):
    def load_notes(self):
        if not apofile.exists():
            self.apodata = {}
            return
        try:
            with apofile.open(mode='rb') as f:
                self.apodata = pickle.load(f)
        except ValueError:
            with apofile.open(mode='r') as f:
                self.apodata = pickle.load(f)

    def save_notes(self):
        with apofile.open(mode='wb') as f:
            pickle.dump(self.apodata, f, protocol=2)
