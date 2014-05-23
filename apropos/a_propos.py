def apropos(log=None, toolkit='qt'):
    """start de GUI op.

    Importeert hiervoor de toolkit-specifieke code
    """
    if toolkit == 'qt':
        from .apropos_qt import main
    elif toolkit == 'wx':
        from apropos_wx import main
    else:
        raise ValueError('Unknown GUI-toolkit specification: '
            'currently only `qt` or `wx` are supported')
    if log:
        main(log=True)
    else:
        main()

if __name__ == "__main__":
    apropos()
