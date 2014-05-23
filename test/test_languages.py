"""
Test stuff for multi language support
"""
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apropos.apomixin import languages

class TestLanguages(unittest.TestCase):

    def test_keys(self):
        self.assertEqual(sorted([x for x in languages.keys()]), ['dutch', 'eng'])

    def test_dutch(self):
        self.assertEqual(languages['dutch']['language'], 'Nederlands')

    def test_english(self):
        self.assertEqual(languages['eng']['language'],'English')

if __name__ == '__main__':
    unittest.main()
