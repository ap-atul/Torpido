import gc
from queue import Queue, Empty
from threading import Thread
from time import sleep

import cv2

from torpido.config.constants import VIDEO_WIDTH
from torpido.util import resize


class Stream:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread, which actually speeds up the video
    reading 2 times faster than working in the main UI Thread.

    Attributes
    ----------
    __Q : queue
        python queue for storing the frames that are to be processed
    stream : video capture
        open cv stream object that read the video in frames
    stopped : bool
        stream is ended or the video is not ended yet

    Examples
    --------
    Reads the video using the Thread and saving the frames in the queue
    to process them. As the video is read by the Thread the speed increases
    and locking functions of open cv can be skipped.
    """

    def __init__(self, src):
        cv2.setUseOptimized(True)
        self.__Q = Queue(maxsize=1200)
        self.stream = cv2.VideoCapture(src)
        self.stopped = False
        self._thread = None

    def start(self):
        self._thread = Thread(target=self.__get, name="torpido.video.Stream", args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    def __get(self):
        while True:
            if self.stopped:
                break

            if not self.__Q.full():
                (grabbed, frame) = self.stream.read()

                if not grabbed:
                    self.stream.release()
                    self.stopped = True
                    return

                # resizing the reduce memory and since im not using full
                frame = resize(frame, width=VIDEO_WIDTH)
                self.__Q.put(frame)

            else:
                sleep(0.1)

        self.stream.release()

    def read(self):
        try:
            data = self.__Q.get()
        except Empty:
            data = None
        return data

    def get_capture(self):
        return self.stream

    def get_queue_size(self):
        return self.__Q.qsize()

    def more(self):
        return not self.stopped

    def stop(self):
        self.stopped = True
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self.stream.release()
        gc.collect()

    def __del__(self):
        del self.__Q
