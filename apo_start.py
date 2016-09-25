"""Starter for the apropos application

imports the main class from apropos/apropos.py and calls it
optional arguments to turn logging on and/or provide a window title
"""
import sys
import argparse
from apropos.a_propos import apropos

parser = argparse.ArgumentParser(description='Simple notes application')
parser.add_argument('-l', '--log', action='store_true', help='enable logging')
parser.add_argument('-n', '--title', help="provide a title for the window")
args = parser.parse_args()
apropos(log=args.log, title=args.title)

