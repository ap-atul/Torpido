import threading
from lib.visual import startProcessing

file = 'examples/example4.mp4'
t1 = threading.Thread(target=startProcessing, args=(file, ))
t1.start()

# merge and cal sum of two dict()
# z = dict(Counter(x)+Counter(y))
