from apropos_wx import Main

class Apropos(Main):
    def __init__(self, arg=None):
        if arg is not None:
            Main.__init__(self, logging=True)
        else:
            Main.__init__(self)

if __name__ == "__main__":
    Apropos()
