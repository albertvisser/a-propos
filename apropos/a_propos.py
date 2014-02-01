from .apropos_qt import Main
## from apropos_wx import Main

class Apropos(Main):
    """main class die overerft van de main class in de gui afhankelijke code
    """
    def __init__(self, arg=None):
        if arg is not None:
            Main.__init__(self, log=True)
        else:
            Main.__init__(self)

if __name__ == "__main__":
    Apropos()
