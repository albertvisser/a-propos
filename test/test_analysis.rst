===============================
Unittesting the apropos project
===============================

source files to possibly test:
==============================

__init__.py
-----------

this file is empty, so nothing to test here.
I'm wondering if we even need it.

apo_start.pyw
-------------

this is all module level code that does no more than import from the main
program and execute the main class.
Not useful to test separately.

apropos/__init__py
------------------

this file is empty, nothing to test here.
It is implicitely tested by the import in apo_start.py

apropos/nl.py
-------------

the symbol definition in this file can be tested by running test_languages.py

apropos/en.py
-------------

the symbol definition in this file can be tested by running test_languages.py

apropos/a_propos.py
-------------------

the function definition in this file can be tested by running apo_test.py which
contains various call formats.
The easiest way to check what happens in the different situations is to insert
appropriate print statements in the main() functions of apropos_wx.py and
apropos_qt.py. This can show both which type of toolkit is used and if logging is
used.

apropos/apomixin.py
-------------------

The module level code in this file can be unit tested by importing it and
looking at the `languages` dictionary.
This is done when running test_languages.py

The class definition in this file can be tested by instantiating the class and
testing the load_notes and save_notes methods.
This is done when running test_apomixin.py

    side note: wouldn't we want to know the file has the wrong type of data?

apropos/apropos_wx.py
---------------------

The module level code in this file can be tested by executing `a_propos.py` through
`apo_test.py` which will use a `toolkit` argument of value 'wx' and various values
for the `log` argument.

The Page class can be tested by creating an instance of it and checking if a
wxPanel is created with a full-size wxTextCtrl on it. Currently there are no methods
defined for it here, so nothing more to test.

The Checkdialog class can be tested by creating an instance of it and checking if a
wxDialog is created containing a text, a checkbox and an OK button; the text is
provided through the `message` parameter on creation; the text for the check button is
taken from the parent's language setting.

The MainFrame class itself can be tested by creating an instance of it and checking if
a wx.Frame is created that has a specific icon and a wxPanel containing a wxNotebook
with contents created by the `initapp` method.

can unit tests for these methods be done by just calling them after instantiating the
MainFrame class (I think they should be but does it work)?

Possibly if I call the methods that need it with a parameter set to an object that has
the properties of an event, so a Skip() method and other stuff

Maybe this will work as a general approach:

1. define an object that has the properties of an event, insofar as that these
   properties are used in the method to be tested. What the properties do or mean
   should be constructive in running the test.
2. use this object as a parameter when calling the method.

* *the page_changed method* is run by creating the MainFrame so its
  technically-correctness is automatically checked. The test should:

    * run with a parameter that has getSelection (returning a page number) and a Skip
      method (that just needs to show it has executed)
    * check the class's `current` attribute
    * check the application's focus
    * the skip method should have run

* *the on_left_release method*'s test should:

    * run with a parameter that has a Skip method (that just needs to show it has
      executed)
    * check the application's focus
    * the skip method should have run

* *the on_key method*'s test should:

    * run with a parameter that has a Skip method (that just needs to show it has
    executed) and also GetKeyCode and GetModifiers methods that return an integer value
    * this method has various results that are probably best viewed in the gui itself:

        * on Ctrl-L the application's state should be identical to the one at the start
          of the run. Note that this is accomplished by calling the `initapp` method.
        * on Ctrl-N the application's state should be one tab more than before, with no
          text. Note that this is accomplished by calling the `newtab` method.
        * on Ctrl-W the application's state should be one tab less than before. Note
          that this is accomplished by calling the `closetab` method.
        * on Ctrl-H, dependent on a setting, a dialog is shown or not. After that, the
          application is hidden. Following the dialog and dependent on the choice made,
          the aforementioned setting is modified. Apart from these, the application's
          state is unchanged. An icon is created in the systray.
        * on Ctrl-S, the save file is changed. Dependent on a setting, a dialog is shown.
          Dependent on the choice maide in the dialog, this setting is modified.
          Note that the saving is accomplished by calling the `afsl` method.
        * on Ctrl-Q, the save file is changed and the application is terminated.
          Note that the saving is accomplished by calling the `afsl` method.
        * on Ctrl-F1, a dialog is shown. Dependent on the choice made, the language
          setting is changed. Note that this is accomplished by calling the
          `choose_language` method.
        * on F1, a dialog is shown containing the help text and an ok button (by calling
          the `helppage` method.). After that, the application's state is unchanged.
        * on F2, a dialog is shown showing the current tab's title and Ok and Cancel
          buttons. On ok, the current tab's title should change to the text in the
          dialog. Note that this is accomplished by calling the `asktitle` method.
        * on Esc, the save file is changed and the application is terminated. Note
          that the saving is accomplished by calling the `afsl` method.
    * the skip method should have run except in the case of Ctrl-W

* *the on_left_doubleclick method*'s test should:

    * run with a parameter that has a Skip method (that just needs to show it has
    executed) and also GetX and GetY methods that return an integer value
    * check that a page has been deleted
    * check that the skip method has been run

* *the initapp method*  is run by creating the MainFrame so its
  technically-correctness is automatically checked. The test should:

    * check the `opts` attribute (set to a dictionary containing the application
      settings)
    * check the `apodata` attribute (set to a dictionary containing the application
      settings as the zeroeth item and the tab titles and texts as the first and next
      ones)
    * check if there are pages according to what's in the data file (created through the
      `newtab` method)
    * check the `current` attribute

* *the newtab method*'s test should:

    * check that a new page is created with empty text and title numbered according to
      the current number of pages plus one
    * if called with a first or `titel` argument: that the title is set to the argument
      value
    * if called with a second or `note` argument: that the text is set to the argument
      value

* *the closetab method*'s test should:

    * if there was only one tab:

        * check that the file has been changed
        * check that the application has terminated

    * otherwise:

        * check that a page has been deleted

* *the revive method*'s test should:

    * run with a parameter that has a Skip method (that just needs to show it has
      executed)
    * check that the application is shown again
    * check that the applications further state is unchanged
    * check that the icon in the systray disappears

* *the afsl method*'s test should:

    * run with a parameter that has a Skip method (that just needs to show it has
      executed)
    * check that the `opts` and `apodata` attributes are correcttly updated
    * check that the file is changed
    * check that the skip method is called

* *the helppage method*'s test should:

    * check that a dialog is created with the correct title and text

* *the asktitle method*'s test should:

    * check that a dialog is created with the correct title
    * check that the text is taken from the correct tab's title
    * check that, when ok is pressed, the (modified) text is used to modify the
      correct tab's title

* *the choose_language method*'s test should:

    * check that the choose language dialog is shown with the correct title and the
      right language selected
    * check that the language setting is correctly modified


apropos/apropos_qt.py
---------------------

The module level code in this file can be tested by executing `a_propos.py`
with a `toolkit` argument of value 'qt' and various values of the `log` argument.


The Page class can be tested by creating an instance of it and checking if a
QFrame is created with a full-size QTextEdit on it.

*   *the keyPressEvent method* can be tested by calling it with a parameter that has
    attributes that are required by the `on_key` method.
*   *the on_key method* can be tested by calling it with a parameter that has methods
    `key` and `modifiers`. The following situations can occur:

        *   for Alt-Left the previous tab should be selected (through the MainFrame's
            `goto_previous` method)
        *   for Alt-Right the next tab should be selected (through the MainFrame's
            `goto_next` method)

**These methods should be refactored by defining actions on the MainFrame class with
shortcuts to the mentioned key-combo's**

The Checkdialog class can be tested by creating an instance of it and checking if a
QDialog is created containing a text, a checkbox and an OK button; the text is provided
through the `message` parameter on creation; the text for the checkbox is taken from the
parent's language setting.

*   *the klaar method*'s test should:

    * update the MainFrame's `opts` attribute when the checkbox's value is changed
    * close he dialog

The MainFrame class itself can be tested by creating an instance of it and checking if
a QMainWindow is created that has a specific icon and a QTabWidget with contents created
by the `initapp` method.

*   *the page_changed method*'s test should:

    *   be called with or without a parameter that mimicks the event (but is not used)
    *   check for modification of the `current` attribute
    *   check for changing the focus to the corresponding tab

*   *the keyPressEvent method*'s test should:

    *   be called with a parameter that has attributes that are required by the `on_key`
        method.

*   *the on_key method*'s test should:

    *   be called with a parameter that has methods `key` and `modifiers`. The following
        situations can occur:

        * on Ctrl-L the application's state should be identical to the one at the start
          of the run.  Note that this is accomplished by calling the `initapp` method.
        * on Ctrl-N the application's state should be one tab more than before, with no
          text. Note that this is accomplished by calling the `newtab` method.
        * on Ctrl-W the application's state should be one tab less than before.  Note
          that this is accomplished by calling the `closetab` method.
        * on Ctrl-H, dependent on a setting, a dialog is shown or not. After that, the
          application is hidden. Following the dialog and dependent on the choice made,
          the aforementioned setting is modified. Apart from these, the application's
          state is unchanged. An icon is created in the systray.
        * on Ctrl-S, the save file is changed. Dependent on a setting, a dialog is shown.
          Dependent on the choice made in the dialog, this setting is modified. Note that
          the saving is accomplished by calling the `afsl` method.
        * on Ctrl-Q, the save file is changed and the application is terminated.  Note
          that the saving is accomplished by calling the `afsl` method.
        * on Ctrl-F1, a dialog is shown. Dependent on the choice made, the language
          setting is changed. Note that this is accomplished by calling the
          `choose_language` method.
        * on F1, a dialog is shown containing the help text and an ok button (by calling
          the `helppage` method. After that, the application's state is unchanged.
        * on F2, a dialog is shown showing the current tab's title and Ok and Cancel
          buttons. On ok, the current tab's title should change to the text in the
          dialog. Note that this is accomplished by calling the `asktitle` method.
        * on Esc, the save file is changed and the appication is terminated. Note that
          the saving is accomplished by calling the `newtab` method.

**The previous two methods should be refactored by defining actions on the MainFrame
class with shortcuts to the mentioned key-combo's**

* *the initapp method*  is run by creating the MainFrame so its
  technically-correctness is automatically checked. The test should:

    * check the `opts` attribute (set to a dictionary containing the application
      settings)
    * check the `apodata` attribute (set to a dictionary containing the application
      settings as the zeroeth item and the tab titles and texts as the first and next
      ones)
    * check if there are pages according to what's in the data file (created through the
      `newtab` method)
    * check the `current` attribute

* *the newtab method*'s test should:

    * check that a new page is created with empty text and title numbered according to
      the current number of pages plus one
    * if called with a first or `titel` argument: that the title is set to the argument
      value
    * if called with a second or `note` argument: that the text is set to the argument
      value

* *the goto_previous method*'s test should:

    * check that the currentIndex is decremented by one if possible
    * check that the focus is set to the corresponding tab


* *the goto_next method*'s test should:

    * check that the currentIndex is incremented by one if possible
    * check that the focus is set to the corresponding tab

* *the closetab method*'s test should:

    * if there was only one tab:

        * check that the file has been changed
        * check that the application has terminated

    * otherwise:

        * check that the page indicated in the calling paremeter has been deleted

* *the revive method*'s test should:

    * run with a parameter that mimicks a tray_icon event
    * check that a message appears on a hover event
    * check that the application is shown again on a click event
    * check that the application's further state is unchanged
    * check that the icon in the systray disappears

* *the closeEvent method*'s test should:

    * run with a parameter that mimicks an close event
    * chack that it calls the `afsl` method

* *the afsl method*'s test should:

    * check that the `opts` and `apodata` attributes are correcttly updated
    * check that the file is changed

* *the helppage method*'s test should:

    * check that a dialog is created with the correct title and text (by calling the
      `meld` method)

* *the meld method*'s test should:

    * check that a messagebox is created with the specified title and the message passed
      in the argument.

* *the asktitle method*'s test should:

    * check that a dialog is created with the correct title
    * check that the text is taken from the correct tab's title
    * check that, when ok is pressed, the (modified) text is used to modify the
      correct tab's title

* *the choose_language method*'s test should:

    * check that the choose language dialog is shown with the correct title and the
      right language selected
    * check that the language setting is correctly modified

----

TODO: rewrite to describe what the various test modules do

e.g.

test/apo_test.py
----------------

this is all module level code that shows the various call formats
can be used to test if they do the right thing(s).
