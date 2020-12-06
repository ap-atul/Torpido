"""
This file reads the video and gives ranking to frames
that have motion in it, saves in the dictionary with frame numbers
this dictionary is then saved in a joblib file defined in constants.py
"""

import time

import cv2
import numpy as np

from torpido.config import *
from torpido.video import VideoGet


class Visual:
    """
    Class to perform Visual Processing on the input video file. Motion and Blur detections
    are used to calculate the rank. The ranks are per frame, so later the ranks are
    normalized to sec

    Attributes
    ----------
    self.__blurThreshold : int
        threshold to rank the blur feature
    self.__motionThreshold : int
        threshold to rank the motion feature
    self.__fps : float
        input video fps
    self.__frameCount : int
        number of frames
    self.__motion : list
        list of the ranks for the motion feature
    self.__blur : list
        list of the ranks for the blur feature
    self.__cache : Cache
        cache object to store the data
    self.__videoGetter : VideoGet
        video reader object to read the video and save it in thread
    """

    def __init__(self):
        cv2.setUseOptimized(True)
        self.__blurThreshold = BLUR_THRESHOLD
        self.__motionThreshold = MOTION_THRESHOLD
        self.__fps = None
        self.__frameCount = None
        self.__motion = None
        self.__blur = None
        self.__cache = Cache()
        self.__videoGetter = None
        self.__videoPipe = None

    def __detectBlur(self, image):
        """
        Laplacian take 2nd derivative of one channel of the image(gray scale)
        It highlights regions of an image containing rapid intensity changes, much like the Sobel and Scharr operators.
        And then calculates the variance (squared SD), then check if the variance satisfies the Threshold value/

        Parameters
        ---------
        image : array
            frame from the video file
        """
        # if blur rank is 0 else RANK_BLUR
        if cv2.Laplacian(image, cv2.CV_64F).var() >= self.__blurThreshold:
            return 0
        return RANK_BLUR

    def __timedRankingNormalize(self):
        """
        Since ranking is added to frames, since frames are duration * fps
        and audio frame system is different since frame are duration * rate
        so we need to generalize the ranking system
        sol: ranking sec of the video and audio, for than taking mean of the
        frames to generate rank for video.

        Since ranking is 0 or 1, the mean will be different and we get more versatile
        results.

        We will read both the list and slice the video to get 1 sec of frames(1 * fps) and get
        mean/average as the rank for the 1 sec

        """
        motionNormalize = []
        blurNormalize = []
        for i in range(0, int(self.__frameCount), int(self.__fps)):
            if len(self.__motion) >= (i + int(self.__fps)):
                motionNormalize.append(np.mean(self.__motion[i: i + int(self.__fps)]))
                blurNormalize.append(np.mean(self.__blur[i: i + int(self.__fps)]))
            else:
                break

        # saving all processed stuffs
        self.__cache.writeDataToCache(CACHE_RANK_MOTION, motionNormalize)
        self.__cache.writeDataToCache(CACHE_RANK_BLUR, blurNormalize)
        Log.d(f"Visual rank length {len(motionNormalize)}  {len(blurNormalize)}")
        Log.i(f"Visual ranking saved .............")

    def __setVideoFps(self):
        """
        Function to set the original video fps to cache
        """
        self.__cache.writeDataToCache(CACHE_FPS, self.__fps)

    def __setVideoFrameCount(self):
        """
        Function to set the original video frame count to cache
        """
        self.__cache.writeDataToCache(CACHE_FRAME_COUNT, self.__frameCount)

    def __del__(self):
        """
        Clean ups
        """
        del self.__cache
        if self.__videoGetter is not None:
            del self.__videoGetter

        Log.d("Cleaning up.")

    def startProcessing(self, pipe, inputFile, display=False):
        """
        Function to run the processing on the Video file. Motion and Blur features are
        detected and based on that ranking is set

        Parameters
        ----------
        pipe : Communication link
            set progress on the ui
        inputFile : str
            input video file
        display : bool
            True to display the video while processing
        """

        if os.path.isfile(inputFile) is False:
            Log.e(f"File {inputFile} does not exists")
            return

        # maintaining the motion and blur frames list
        self.__motion = list()
        self.__blur = list()

        self.__videoGetter = VideoGet(str(inputFile)).start()
        myClip = self.__videoGetter.stream

        if self.__videoGetter.getQueueSize() == 0:
            time.sleep(1)
            Log.d(f"Waiting for the buffer to fill up.")

        fps = myClip.get(cv2.CAP_PROP_FPS)
        totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)

        self.__fps = fps
        self.__frameCount = totalFrames
        self.__setVideoFps()
        self.__setVideoFrameCount()

        # printing some info
        Log.d(f"Total count of video frames :: {totalFrames}")
        Log.i(f"Video fps :: {fps}")
        Log.i(f"Bit rate :: {cv2.CAP_PROP_BITRATE}")
        Log.i(f"Video format :: {cv2.CAP_PROP_FORMAT}")
        Log.i(f"Video four cc :: {cv2.CAP_PROP_FOURCC}")

        count = 0
        firstFrame = self.__videoGetter.read()
        firstFrameProcessed = True

        while self.__videoGetter.more():
            frame = self.__videoGetter.read()

            if frame is None:
                break

            original = frame
            count += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.__blur.append(self.__detectBlur(frame))
            frame = cv2.GaussianBlur(frame, (21, 21), 0)

            if firstFrameProcessed:
                firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
                firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
                firstFrameProcessed = False

            frameDelta = cv2.absdiff(firstFrame, frame)
            thresh = cv2.threshold(frameDelta, self.__motionThreshold, 255, cv2.THRESH_BINARY)[1]

            threshMax = np.max(thresh)
            if threshMax > 0:
                self.__motion.append(RANK_MOTION)
            else:
                self.__motion.append(0)

            if display:

                # adding the frame to the pipe
                if self.__videoPipe is not None:
                    self.__videoPipe.put(original)

                # not a ui request, so this works
                else:
                    cv2.imshow("Video Output", original)
                    # if the `q` key is pressed, break from the loop

            # assigning the processed frame as the first frame to cal diff later on
            firstFrame = frame

            # setting progress on the ui
            if pipe is not None:
                pipe.send(float((count / totalFrames) * 100))

        # completing the progress
        if pipe is not None:
            pipe.send(100.0)

        # clearing memory
        myClip.release()
        self.__videoGetter.stop()

        # calling the normalization of ranking
        self.__timedRankingNormalize()

    def setPipe(self, pipe):
        """
        Send video frame to the ui threads for displaying, since open cv
        is using the Qt backend, it should be in the main ui thread or else
        the im show does not work in the sub process

        Parameters
        ----------
        pipe : some queue
            add frames and continuous read to the ui display
        """
        self.__videoPipe = pipe
