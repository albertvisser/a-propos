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

Usage
-----

The root of this repo contains a file called `apo_start.pyw` which - as the name
suggests - starts the application. There are no parameters.
The notes file is loaded from the directory you started the application from,
and is created if it isn't present.
