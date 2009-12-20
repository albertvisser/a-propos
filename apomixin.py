import os, pickle
apofile = "apropos.ini"

class Apomixin_test(object):
    def load_notes(self):
        print "gebruik de mixin methode"
        self.apodata = {}

    def save_notes(self):
        print "gebruik de mixin methode"
        for x,y,z in [(x,y[0],y[1]) for x,y in self.apodata.items()]:
            print "%s :-> %s %s" % (x,y,z)
        pass

class Apomixin(object):
    def load_notes(self):
        ## print "gebruik de eigen methode"
        if os.path.exists(apofile):
            f = open(apofile)
            self.apodata = pickle.load(f)
            f.close()
        else:
            self.apodata = {}

    def save_notes(self):
        ## print "gebruik de eigen methode"
        f = open(apofile,"w")
        pickle.dump(self.apodata,f)
        f.close()
