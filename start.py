#! /usr/bin/env python3
"""Starter for the apropos application
"""
import argparse
from apropos.main import apropos

parser = argparse.ArgumentParser(description='Simple notes application')
parser.add_argument('-f', '--file', help='path to the data file (defaults to '
                                         '`apropos.apo` in the startup directory)')
parser.add_argument('-t', '--title', help="provide a title for the window")
args = parser.parse_args()
apropos(fname=args.file, title=args.title)
