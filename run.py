""" For command line testing """

import sys

from torpido.controller import Controller

if len(sys.argv) > 1:
    control = Controller()
    control.start_processing(None, sys.argv[1])
else:
    print("Ah! Funny ;) ;)")
