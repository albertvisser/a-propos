"""start a-propos app

argumenten: filenaam, toolkit, venstertitel
"""

def apropos(file='', toolkit='qt', title=''):
    """start de GUI op.

    Importeert hiervoor de toolkit-specifieke code
    """
    if toolkit == 'qt4':
        from .apropos_qt4 import main
    elif toolkit == 'qt':
        from .apropos_qt5 import main
    elif toolkit == 'wx':
        from apropos_wx import main
    else:
        raise ValueError('Unknown GUI-toolkit specification: '
            'currently only `qt(5)` and `wx` are supported')
    main(file=file, title=title)

if __name__ == "__main__":
    apropos()
