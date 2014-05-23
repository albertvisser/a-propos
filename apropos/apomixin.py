# -*- coding: utf-8 -*-

import os
import sys
import pickle
if sys.version >= '3':
    from apropos import en, nl
else:
    import en, nl
apofile = "apropos.pck"

languages = {}
languages.update(en.lang)
languages.update(nl.lang)

class ApoMixin(object):
    def load_notes(self):
        if not os.path.exists(apofile):
            self.apodata = {}
            return
        try:
            with open(apofile, 'rb') as f:
                self.apodata = pickle.load(f)
        except ValueError:
            with open(apofile, 'r') as f:
                self.apodata = pickle.load(f)

    def save_notes(self):
        with open(apofile, 'wb') as f:
            pickle.dump(self.apodata, f, protocol=2)
