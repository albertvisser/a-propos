A propos
========

Apropos is a simple interface for keeping notes.
I've intentionally tried to keep it pretty simple.

The interface looks something like this::

     ---------
     | 1 | 2 |
    |-------------------------------------------|
    |                                           |
    |                                           |
    |                                           |
    |                                           |
    |                                           |
    |                                           |
    |                                           |
    |-------------------------------------------|


The notes are automatically loaded on startup, and saved on exit.
No need (or possibility) to choose a file name.

It has the following functions, activated by keyboard shortcuts:

- create a new tab
- (re)name the current tab
- delete the current tab
- switch to the next tab on the right-hand side
- switch to the next tab on the left-hand side
- save all tabs
- load all tabs
- hide the application in the system tray
- exit the application
- list all keyboard shortcuts
- change language (for help and such)

Usage
-----

The root of this repo contains a file called ``apo_start.pyw`` which - as the name
suggests - starts the application. It can be called without parameters, or with
a filename.
If no name is given, the notes file is loaded from the directory you started
the application from- using a standard name - and is created if it isn't present.
It's possible to have what explanatory texts there are displayed in a language of
choice, however currently only Dutch and English are available.

To make this application work under Python 3 I had to change GUI toolkits so I made
a PyQt version.
To change back to the wx version simply change the import in a_propos.py and call
apo_start using Python 2.

Requirements
------------

- Python
- PyQt4 for the Python 3 version
- wxPython for the Python 2 version

Note that the current implementation uses *pickle* for storing the data, I'm in the
process of changing that to something safer.
