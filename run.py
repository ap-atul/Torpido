import sys

from controller import Controller

if len(sys.argv) > 1:
    control = Controller()
    control.saveLogs(True)
    control.startProcessing(sys.argv[1], True)
else:
    print("Ah! Funny ;) ;)")
