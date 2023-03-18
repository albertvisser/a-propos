"""apropos: importer voor de in de toolkit configuratie bepaalde implementatie(s)
"""
from .toolkit import toolkit

if toolkit == 'qt':
    from .gui_qt import AproposGui, CheckDialog, OptionsDialog
elif toolkit == 'gtk':
    from .gui_gtk import AproposGui, CheckDialog, OptionsDialog
elif toolkit == 'wx':
    from .gui_wx import AproposGui, CheckDialog, OptionsDialog
