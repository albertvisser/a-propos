"""Various formats for starting up the application
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apropos.a_propos import apropos

## apropos() # basic call: qt version, no logging

## apropos(True) # truthy first argument: qt version with logging
## apropos(False) # falsey first argument: qt version without logging

## apropos(True, True) # truthy first and second argument: error unknown toolkit

## apropos(True, 'qt') # qt version specified with logging
## apropos(True, 'wx') # wx version specified with logging

## apropos(toolkit=True) # error unknown toolkit
## apropos(toolkit='qt') # qt version specified without logging
apropos(toolkit='wx') # wx version specified without logging

## # test first keyword argument
## apropos(log=True) # default qt version with logging requested
## apropos(log=False) # default qt version with no logging requested


