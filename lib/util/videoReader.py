import gc
from queue import Queue
from threading import Thread

import cv2
import imutils

from lib.util.constants import VIDEO_WIDTH


class VideoGet:

    # Class that continuously gets frames from a VideoCapture object
    # with a dedicated thread, which actually speeds up the video
    # reading 2 times faster than working in the main UI Thread.

    def __init__(self, src):
        """
        initialize with the input file to read
        :param src: string, input file
        """
        self.Q = Queue()
        self.stream = cv2.VideoCapture(src)
        self.stopped = False

    def start(self):
        """
        create the thread
        :return: class instance
        """
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        """
        read the frame from the stream, much faster
        in the thread
        :return: None
        """
        while True:
            if self.stopped:
                return

            if not self.Q.full():
                (grabbed, frame) = self.stream.read()

                if not grabbed:
                    self.stop()
                    return

                frame = imutils.resize(frame, width=VIDEO_WIDTH)
                self.Q.put(frame)

    def read(self):
        """
        get the frame from the queue
        :return: frame
        """
        return self.Q.get()

    def getCapture(self):
        """
        get the entire stream
        :return: reads open cv object
        """
        return self.stream

    def more(self):
        """
        checking if there is space in the Q
        :return: bool
        """
        return not self.stopped

    def stop(self):
        """
        stop reading the source
        :return: none
        """
        self.stopped = True
        gc.collect()
        self.stream.release()
