"""apropos: importer voor de in de toolkit configuratie bepaalde implementatie(s)
"""
from .toolkit import toolkit

if toolkit == 'qt':
    from .gui_qt import AproposGui, CheckDialog, OptionsDialog
elif toolkit == 'gtk':
    # from .gui_gtk import AproposGui, CheckDialog, OptionsDialog
    # from .gui_gtk_poging1a import AproposGui, CheckDialog, OptionsDialog
    # from .gui_gtk_poging2 import AproposGui, CheckDialog, OptionsDialog
    raise ValueError("Gtk ondersteumt het opstarten vanuit de applicatielogica niet,"
                     " dus kan ik geen Gtk variant ondersteunen")
elif toolkit == 'wx':
    from .gui_wx import AproposGui, CheckDialog, OptionsDialog
