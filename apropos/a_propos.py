"""start a-propos app

argumenten: filenaam, venstertitel indien gewenst
"""
from .toolkit import toolkit


def apropos(fname='', title=''):
    """start de GUI op.

    Importeert hiervoor de toolkit-specifieke code
    """
    print('working with', toolkit)
    if toolkit == 'qt':
        from .gui_qt import main
    elif toolkit == 'gtk':
        from .gui_gtk import main
    elif toolkit == 'wx':
        from .gui_wx import main
    else:
        raise ValueError('Unknown GUI-toolkit specified `{}`; '
                         'currently only `qt`, `gtk` and `wx` are supported'.format(toolkit))
    main(fname=fname, title=title)
