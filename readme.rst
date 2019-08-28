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

The root of this repo contains a file called ``start.py`` which - as the name
suggests - starts the application. It can be called without parameters, or with
a filename.
If no name is given, the notes file is loaded from the directory you started
the application from- using a standard name - and is created if it isn't present.

Functionality is not guaranteed for Python < 3.5

It's possible to have what explanatory texts there are displayed in a language of
choice, however currently only Dutch and English are available.

Some history
------------
I started building this app using wxPython. To make it work under Python 3 I had to change GUI toolkits so I made a PyQt version.

Since the release of wxPhoenix, the wxPython version was reinstated and brought up-to-date. Just for kicks I also wrote a Gtk version.

Requirements
------------

- Python
- either PyQt5, wxPython (>=4) or Gtk (3) for the GUI part
  

Note that the current implementation uses *pickle* for storing the data, I'm in the
process of changing that to something safer.
