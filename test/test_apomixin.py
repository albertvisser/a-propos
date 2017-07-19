"""
Test stuff for the ApoMixin class
"""
import os
import sys
import pathlib
import pickle
import copy
import unittest
from apropos.apomixin import apofile, ApoMixin
basedir = pathlib.Path(__file__).parent.joinpath('..')
sys.path.append(basedir)
testdumpfile = pathlib.Path('apropos_test.pck')


class TestApoMixin(unittest.TestCase):
    "Test class for ApoMixin"

    def setUp(self):
        """
        create some data and an ApoMixin object
        """
        self.data = {
            1: {"aaa": "aaaaaaaa", "bbb": "bbbbbbbb", "ccc": "cccccccc"},
            2: {"ddd": "dddddddd", "eee": "eeeeeeee", "fff": "ffffffff"}}
        self.test = ApoMixin()

    def test_load_notes_happy_flow(self):
        """
        pickle and save the data under the name defined in `apofile`;
        run the load_notes method; compare the mixin's `apodata` attribute
        with the original data (must have the same value).
        """
        with apofile.open(mode='wb') as f:
            pickle.dump(self.data, f, protocol=2)
        self.test.load_notes()
        self.assertEqual(self.test.apodata, self.data)

    def test_load_notes_file_not_found(self):
        """
        run the load_notes method with no existing file; compare the mixin's
        `apodata` attribute with the original data (must be an empy dict).
        """
        self.test.load_notes()
        self.assertEqual(self.test.apodata, {})

    def test_load_notes_not_a_pickle(self):
        """
        run the load_notes method with a non-pickle file; compare the mixin's
        `apodata` attribute with the original data (must raise an exception).
        """
        with apofile.open(mode='w') as f:
            f.write("oihgyavjjvjdvj  diidn dnni")
            f.write("\n")
        error = pickle.UnpicklingError if sys.version >= '3' else IndexError
        self.assertRaises(error, self.test.load_notes)

    def test_save_notes_happy_flow(self):
        """
        pickle and save the data under the a name not equal to `apofile`;
        copy the data into the mixin's `apodata` attribute, run the save_notes
        method and compare the created files (should have identical contents);
        optionally load and unpickle both files and compare the results
        (should also be the same value).
        """
        with testdumpfile.open(mode='wb') as f:
            pickle.dump(self.data, f, protocol=2)
        self.test.apodata = copy.deepcopy(self.data)
        self.test.save_notes()
        with testdumpfile.open(mode='rb') as f1, apofile.open(mode='rb') as f2:
            contents1 = f1.read()
            contents2 = f2.read()
        self.assertEqual(contents2, contents1)

    def tearDown(self):
        """
        if a savefile exists, delete it
        """
        error = FileNotFoundError if sys.version >= '3.3' else OSError
        try:
            os.remove(apofile)
        except error:
            pass
        try:
            os.remove(testdumpfile)
        except error:
            pass

if __name__ == '__main__':
    unittest.main()
