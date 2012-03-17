import sys
from apropos.apropos import Apropos
if len(sys.argv) > 1:
    Apropos(sys.argv[1])
else:
    Apropos()
