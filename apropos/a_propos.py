"""start a-propos app

argumenten: filenaam, venstertitel indien gewenst
"""
from .toolkit import toolkit


def apropos(file='', title=''):
    """start de GUI op.

    Importeert hiervoor de toolkit-specifieke code
    """
    if toolkit == 'qt4':
        from .apropos_qt4 import main
    elif toolkit == 'qt':
        from .apropos_qt5 import main
    elif toolkit == 'gtk':
        from .apropos_gtk3 import main
    elif toolkit == 'wx':
        from .apropos_wx import main
    else:
        raise ValueError('Unknown GUI-toolkit specification `{}`: '.format(toolkit)
                         ', currently only `qt(4)`, `gtk` and `wx` are supported')
    main(file=file, title=title)
