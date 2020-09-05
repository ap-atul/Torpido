from threading import Thread

import cv2


class VideoGet:

    # Class that continuously gets frames from a VideoCapture object
    # with a dedicated thread, which actually speeds up the video
    # reading 2 times faster than working in the main UI Thread.

    def __init__(self, src):
        """
        initialize with the input file to read
        :param src: string, input file
        """
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        """
        create the thread
        :return: class instance
        """
        Thread(target=self.get, args=()).start()  # creating a thread
        return self

    def get(self):
        """
        read the frame from the stream, much faster
        in the thread
        :return: array, single frame
        """
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def getCapture(self):
        """
        get the entire stream
        :return: reads open cv object
        """
        return self.stream

    def stop(self):
        """
        stop reading the source
        :return: none
        """
        self.stopped = True
        self.stream.release()
