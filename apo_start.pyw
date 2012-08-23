"""Starter for the apropos application

imports the main class from apropos/apropos.py and calls it
optional argument: anything - to indicate logging is wanted
"""
import sys
from apropos.apropos import Apropos
if len(sys.argv) > 1:
    Apropos(sys.argv[1])
else:
    Apropos()

