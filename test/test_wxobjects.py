"""
Test stuff for the classes in apropos_wx.py
This is just to test the creation of the objects; therefore no event loop is started
"""
import sys
import wx
import unittest
import pathlib
sys.path.append(pathlib.Path(__file__).parent.joinpath('..'))

from apropos.a_propos import apropos
from apropos.apomixin import apofile, languages, ApoMixin
from apropos.apropos_wx import Page, CheckDialog, MainFrame

class TestWxObjects(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frm = wx.Frame(None, -1)

    def test_page(self):
        """
        create a Page instance of Page and check if a wxPanel is created
        with a (full-size) wxTextCtrl on it.
        """
        class Dummy(object):
            """
            this class is needed for proper creation of the Page object
            """
            def on_key(self):
                pass
        hlp = Dummy()
        testobj = Page(self.frm, -1, hlp)
        self.assertIsInstance(testobj, wx.Panel)
        self.assertIsInstance(testobj.txt, wx.TextCtrl)
        self.assertEqual(testobj.txt.Value, "")

    def test_checkdialog(self):
        """
        Create an instance of Checkdialog and check if a wxDialog is created
        containing a text, a checkbox and an OK button; the text is
        provided through the `message` parameter on creation; the text for the
        checkbox is taken from the parent's language setting.
        Unfortunately (?) we can't test the text because there's no reference to it
        """
        title = "Title"
        message = "Very interesting message"
        show_text = languages["eng"]["show_text"]
        self.frm.opts = { "language": "eng" }
        testobj = CheckDialog(self.frm, -1, title, message=message)
        self.assertIsInstance(testobj, wx.Dialog)
        self.assertEqual(testobj.Title, title)
        self.assertIsInstance(testobj.Check, wx.CheckBox)
        self.assertEqual(testobj.Check.LabelText, show_text)
        self.assertIsInstance(testobj.bOk, wx.Button)
        self.assertEqual(testobj.bOk.Id, wx.ID_OK)

    def test_mainframe(self):
        """
        Create an instance of MainFrame and check if a wx.Frame is created
        that has a specific icon and a wxPanel containing a wxNotebook
        with contents created by the `initapp` method.
        """
        testobj = MainFrame(self.frm, -1)
        self.assertIsInstance(testobj, wx.Frame)
        self.assertIsInstance(testobj, ApoMixin)
        self.assertIsInstance(testobj.apoicon, wx.Icon)
        # need to check which icon?
        self.assertIsInstance(testobj.nb, wx.Notebook)
        # need to check the page and text contents also?


if __name__ == '__main__':
    unittest.main()
