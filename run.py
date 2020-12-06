import sys

from controller import Controller

if len(sys.argv) > 1:
    control = Controller()
    control.startProcessing(None, sys.argv[1])
else:
    print("Ah! Funny ;) ;)")

