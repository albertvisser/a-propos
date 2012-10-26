import os
import pickle
import en, nl
apofile = "apropos.ini"

languages = {}
languages.update(en.lang)
languages.update(nl.lang)

class Apomixin(object):
    def load_notes(self):
        if os.path.exists(apofile):
            try:
                with open(apofile, 'rb') as f:
                    self.apodata = pickle.load(f)
            except ValueError:
                with open(apofile, 'r') as f:
                    self.apodata = pickle.load(f)
        else:
            self.apodata = {}

    def save_notes(self):
        f = open(apofile, 'wb')
        pickle.dump(self.apodata, f)
        f.close()
