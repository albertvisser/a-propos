"""Starter for the apropos application

imports the main class from apropos/apropos.py and calls it
optional argument: anything - to indicate logging is wanted
"""
import sys
from apropos.a_propos import apropos
if len(sys.argv) > 1:
    apropos(sys.argv[1])
else:
    apropos()

