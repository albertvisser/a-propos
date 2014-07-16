"""
Test stuff for the MainFrame methods in apropos_wx.py

Trying to do this without an event loop
Let's just ignore the key capturing; it's been rewritten so that for each shortcut
a routine is called. Let's just test these routines
This means that I still have to add a few
"""
import os
import sys
import wx
import pickle
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apropos.apomixin import apofile, languages
from apropos.apropos_wx import MainFrame

keytab = {
    '': (None, None),
    'Ctrl-L' : (ord('L'), wx.MOD_CONTROL),
    'Ctrl-N' : (ord('N'), wx.MOD_CONTROL),
    'Ctrl-W' : (ord('W'), wx.MOD_CONTROL),
    'Ctrl-H' : (ord('H'), wx.MOD_CONTROL),
    'Ctrl-S' : (ord('S'), wx.MOD_CONTROL),
    'Ctrl-Q' : (ord('Q'), wx.MOD_CONTROL),
    'Ctrl-F1' : (wx.WXK_F1, wx.MOD_CONTROL),
    'F1' : (wx.WXK_F1, None),
    'F2' : (wx.WXK_F2, None),
    'Esc' : (wx.WXK_ESCAPE, None),
    }

class Dummy(object):
    """
    multipurpose class simulating event parameters
    """
    def __init__(self, key=''):
        self.skipped = False
        self.key = key
    def GetSelection(self):
        self.pos = 0
        return self.pos
    def GetKeyCode(self):
        return keytab[self.key][0]
    def GetModifiers(self):
        return keytab[self.key][1]
    def GetX(self):
        return 36
    def GetY(self):
        return 20
    def Skip(self):
        self.skipped = True

class TestWxMainFrame(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.testdata = {
            0: {"AskBeforeHide": True, "ActiveTab": 1, 'language': 'eng',
                'NotifyOnLoad': True, 'NotifyOnSave': True},
            1: ('eerste tab', "tekst voor eerste tab"),
            2: ('tweede tab', "tekst voor tweede tab"),
            3: ('derde tab', "tekst voor derde tab"),
            }
        with open(apofile, 'wb') as f:
            pickle.dump(self.testdata, f, protocol=2)
        self.frm = MainFrame(None, -1)

    def test_init(self):
        """
        Create an instance of MainFrame and check if a wx.Frame is created
        that has a specific icon and a wxPanel containing a wxNotebook
        with contents created by the `initapp` method.

        note that self.testdata[0]["ActiveTab"] starts at 0 while the numbering
        of the items in the self.testdata starts at 1
        """
        self.assertEqual(self.frm.nb.PageCount, len(self.testdata) - 1)
        self.assertEqual(self.frm.current, self.testdata[0]["ActiveTab"])
        self.assertEqual(self.frm.nb.GetPageText(self.frm.current),
            self.testdata[self.testdata[0]["ActiveTab"] + 1][0])
        self.assertEqual(self.frm.nb.GetPage(self.frm.current).txt.Value,
            self.testdata[self.testdata[0]["ActiveTab"] + 1][1])

    def test_page_changed(self):
        testobj = Dummy()
        self.frm.page_changed(testobj)
        pos = self.frm.current
        self.assertEqual(self.frm.current, testobj.pos)
        self.assertEqual(testobj.skipped, True)

    def test_on_left_release(self):
        testobj = Dummy()
        self.frm.on_left_release(testobj)
        self.assertEqual(testobj.skipped, True)

    @unittest.skip('maybe temporarily redefine the methods before calling them?')
    def test_on_key(self):
        for key in keytab:
            testobj = Dummy(key)
            self.frm.on_key(testobj)
            self.assertEqual(testobj.skipped, True)

    @unittest.skip('maybe temporarily redefine the method before calling it?')
    def test_left_doubleclick(self):
        testobj = Dummy()
        count = self.frm.nb.PageCount
        self.frm.on_left_doubleclick(testobj)
        self.assertEqual(self.frm.nb.PageCount, count - 1)
        self.assertEqual(testobj.skipped, True)

    def test_load_data(self):
        self.frm.load_data()
        # test result of initapp or the fact that it's been called

    def test_hide_app(self):
        self.frm.hide_app()
        # test if taskbar icon is created

    def test_on_key_save(self):
        self.frm.save_data()
        # test result of afsl or the fact that it's been called

    def test_initapp(self):
        """
        has already been executed in the mainframe's init,
        so just inspect the result"""
        print(self.frm.opts)
        print(self.testdata[0])
        self.assertEqual(self.frm.opts, self.testdata[0])
        for indx in range(self.frm.nb.PageCount):
            self.assertEqual(self.frm.nb.GetPageText(indx),
                self.testdata[indx + 1][0])
            self.assertEqual(self.frm.nb.GetPage(indx).txt.Value,
                self.testdata[indx + 1][1])

    def test_newtab(self):
        number = self.frm.nb.PageCount
        self.frm.newtab()
        self.assertEqual(self.frm.nb.PageCount, number + 1)
        indx = self.frm.nb.PageCount - 1
        self.assertEqual(self.frm.nb.GetPageText(indx), str(number))
        self.assertEqual(self.frm.nb.GetPage(indx).txt.Value, '')

        number = self.frm.nb.PageCount
        titel, note = "nieuwe tab", "tekst voor nieuwe tab"
        self.frm.newtab(titel, note)
        self.assertEqual(self.frm.nb.PageCount, number + 1)
        indx = self.frm.nb.PageCount - 1
        self.assertEqual(self.frm.nb.GetPageText(indx), titel)
        self.assertEqual(self.frm.nb.GetPage(indx).txt.Value, note)

    def test_closetab(self):
        number = self.frm.nb.PageCount
        self.frm.closetab()
        self.assertEqual(self.frm.nb.PageCount, number - 1)

    @unittest.skip("can we test this at all this way?")
    def test_revive(self):
        pass

    def test_afsl(self):
        testobj = Dummy()
        self.frm.afsl(testobj)
        self.assertTrue(os.path.exists(apofile))
        self.assertEqual(testobj.skipped, True)

    @unittest.skip("can't be tested this way - or can it?")
    def test_helppage(self):
        self.frm.helppage()
        # test if instance of wxMessagedialog is created with the specified text

    @unittest.skip("can't be tested this way - or can it?")
    def test_confirm(self):
        self.frm.confirm()
        # test if this runs without extra arguments
        # test with a setting that's false
        # test with a setting that's true: if instance of CheckDialog is created
        #    with the specified text

    @unittest.skip("can't be tested this way - or can it?")
    def test_asktitle(self):
        self.frm.asktitle()
        # test if an instance of wxTextentryDialog is created with the specified text

    @unittest.skip("can't be tested this way - or can it?")
    def test_choose_language(self):
        self.frm.choose_language()
        # test if an instance of wxSingleChoiceDialog is created with the specified contents

    def tearDown(self):
        self.frm.Destroy()
        os.remove(apofile)

if __name__ == '__main__':
    unittest.main()
