from threading import Thread
import cv2


class VideoGet:

    # Class that continuously gets frames from a VideoCapture object
    # with a dedicated thread, which actually speeds up the video
    # reading 2 times faster than working in the main UI Thread.

    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()  # creating a thread
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def getCapture(self):
        return self.stream

    def stop(self):
        self.stopped = True
        self.stream.release()