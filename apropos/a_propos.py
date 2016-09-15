import sys

def apropos(log=None, toolkit='qt', title=''):
    """start de GUI op.

    Importeert hiervoor de toolkit-specifieke code
    """
    if toolkit == 'qt':
        from .apropos_qt import main
    elif toolkit == 'qt5':
        from .apropos_qt5 import main
    elif toolkit == 'wx':
        from apropos_wx import main
    else:
        raise ValueError('Unknown GUI-toolkit specification: '
            'currently only `qt(5)` and `wx` are supported')
    if log:
        main(log=True, title=title)
    else:
        main(title=title)

if __name__ == "__main__":
    apropos()
