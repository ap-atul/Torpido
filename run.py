import sys
from multiprocessing import Lock

from controller import Controller

if len(sys.argv) > 1:
    lock = Lock()
    control = Controller()
    control.saveLogs(True)
    control.startProcessing(lock, sys.argv[1], True)
else:
    print("Ah! Funny ;) ;)")
