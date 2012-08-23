Files in this directory
-----------------------

apo_start.pyw
    starter for the application
    imports sys for sys.argv
    imports from apropos/apropos.py
readme.rst
    description and usage notes
files.rst
    this file

apropos/__init__.py:
    (empty) package indicator
apropos/apomixin.py
    GUI-independent code
    uses pickle to save/load data
apropos/apropos.py
    GUI-independent starter module
    imports from apropos_wx
apropos/apropos_wx.py
    GUI code, wxPython version
    uses wx
    imports from apomixin
apropos/apropos.ico
    application icon
apropos/apropos.xpm
    application icon
