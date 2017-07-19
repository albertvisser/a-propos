"""
Test stuff for multi language support
"""
import sys
import unittest
import pathlib
sys.path.append(pathlib.Path(__file__).parent.joinpath('..'))

from apropos.apomixin import languages


class TestLanguages(unittest.TestCase):
    "Test class"

    def test_keys(self):
        """compare number of keys
        """
        self.assertEqual(sorted([x for x in languages.keys()]), ['dutch', 'eng'])

    def test_dutch(self):
        """check if language file contains correct language
        """
        self.assertEqual(languages['dutch']['language'], 'Nederlands')

    def test_english(self):
        """check if language file contains correct language
        """
        self.assertEqual(languages['eng']['language'], 'English')

if __name__ == '__main__':
    unittest.main()
