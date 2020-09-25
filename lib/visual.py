"""
This file reads the video and gives ranking to frames
that have motion in it, saves in the dictionary with frame numbers
this dictionary is then saved in a joblib file defined in constants.py
"""

import os
import time

import cv2
import numpy as np
from joblib import dump

from lib.util.cache import Cache
from lib.util.constants import *
from lib.util.logger import Log
from lib.util.videoReader import VideoGet


class Visual:
    """
    Class to perform Visual Processing on the input video file. Motion and Blur detections
    are used to calculate the rank. The ranks are per frame, so later the ranks are
    normalized to sec

    Attributes
    ----------
    motionRankPath : str
        file to store the motion rank
    blurRankPath : str
        file to store the blur rank
    blurThreshold : int
        threshold to rank the blur feature
    motionThreshold : int
        threshold to rank the motion feature
    fps : float
        input video fps
    frameCount : int
        number of frames
    motion : list
        list of the ranks for the motion feature
    blur : list
        list of the ranks for the blur feature
    cache : Cache
        cache object to store the data
    videoGetter : VideoGet
        video reader object to read the video and save it in thread
    """

    def __init__(self):
        self.motionRankPath = os.path.join(os.getcwd(), RANK_DIR, RANK_OUT_MOTION)
        self.blurRankPath = os.path.join(os.getcwd(), RANK_DIR, RANK_OUT_BLUR)
        self.blurThreshold = BLUR_THRESHOLD
        self.motionThreshold = MOTION_THRESHOLD
        self.fps = None
        self.frameCount = None
        self.motion = None
        self.blur = None
        self.cache = Cache()
        self.videoGetter = None

    def detectBlur(self, image):
        """
        Laplacian take 2nd derivative of one channel of the image(gray scale)
        It highlights regions of an image containing rapid intensity changes, much like the Sobel and Scharr operators.
        And then calculates the variance (squared SD), then check if the variance satisfies the Threshold value/

        Parameters
        ---------
        image : array
            frame from the video file
        """
        # (h, w) = image.shape
        # (cX, cY) = (int(w / 2.0), int(h / 2.0))
        #
        # fft = np.fft.fft2(image)
        # fftShift = np.fft.fftshift(fft)
        #
        # fftShift[cY - size:cY + size, cX - size:cX + size] = 0
        # fftShift = np.fft.ifftshift(fftShift)
        # recon = np.fft.ifft2(fftShift)
        #
        # magnitude = 20 * np.log(np.abs(recon))
        # mean = np.mean(magnitude)
        # return mean <= thresh
        if cv2.Laplacian(image, cv2.CV_64F).var() >= self.blurThreshold:
            return RANK_BLUR
        return 0

    def startProcessing(self, inputFile, display=False):
        """
        Function to run the processing on the Video file. Motion and Blur features are
        detected and based on that ranking is set

        Parameters
        ----------
        inputFile : str
            input video file
        display : bool
            True to display the video while processing
        """

        if os.path.isfile(inputFile) is False:
            Log.e(f"File {inputFile} does not exists")
            return

        # maintaining the motion and blur frames list
        self.motion = list()
        self.blur = list()

        self.videoGetter = VideoGet(str(inputFile)).start()
        myClip = self.videoGetter.stream

        if self.videoGetter.Q.qsize() == 0:
            time.sleep(1)
            Log.d(f"Waiting for the buffer to fill up.")

        fps = myClip.get(cv2.CAP_PROP_FPS)
        totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)

        self.fps = fps
        self.frameCount = totalFrames
        self.setVideoFps()
        self.setVideoFrameCount()

        # printing some info
        Log.d(f"Total count of video frames :: {totalFrames}")
        Log.i(f"Video fps :: {fps}")
        Log.i(f"Bit rate :: {cv2.CAP_PROP_BITRATE}")
        Log.i(f"Video format :: {cv2.CAP_PROP_FORMAT}")
        Log.i(f"Video four cc :: {cv2.CAP_PROP_FOURCC}")

        count = 0
        firstFrame = self.videoGetter.read()
        firstFrameProcessed = True

        while self.videoGetter.more():
            frame = self.videoGetter.read()

            if frame is None:
                break

            original = frame
            count += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.blur.append(self.detectBlur(frame))
            frame = cv2.GaussianBlur(frame, (21, 21), 0)

            if firstFrameProcessed:
                firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
                firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
                firstFrameProcessed = False

            frameDelta = cv2.absdiff(firstFrame, frame)
            thresh = cv2.threshold(frameDelta, self.motionThreshold, 255, cv2.THRESH_BINARY)[1]

            threshSum = thresh.sum()
            if threshSum > 0:
                self.motion.append(RANK_MOTION)
            else:
                self.motion.append(0)

            if display:
                cv2.imshow("Video Feed", original)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key is pressed, break from the loop
                if key == ord("q"):
                    break

            # assigning the processed frame as the first frame to cal diff later on
            firstFrame = frame

        # clearing memory
        myClip.release()
        self.videoGetter.stop()
        cv2.destroyAllWindows()

        # calling the normalization of ranking
        self.timedRankingNormalize()

    def timedRankingNormalize(self):
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
        for i in range(0, int(self.frameCount), int(self.fps)):
            if len(self.motion) >= (i + int(self.fps)):
                motionNormalize.append(np.mean(self.motion[i: i + int(self.fps)]))
                blurNormalize.append(np.mean(self.blur[i: i + int(self.fps)]))
            else:
                break

        # saving all processed stuffs
        dump(motionNormalize, self.motionRankPath)
        dump(blurNormalize, self.blurRankPath)
        Log.d(f"Visual rank length {len(motionNormalize)}  {len(blurNormalize)}")
        Log.i(f"Visual ranking saved .............")

    def setVideoFps(self):
        """
        Function to set the original video fps to cache
        """
        self.cache.writeDataToCache(CACHE_FPS, self.fps)

    def setVideoFrameCount(self):
        """
        Function to set the original video frame count to cache
        """
        self.cache.writeDataToCache(CACHE_FRAME_COUNT, self.frameCount)

    def __del__(self):
        """
        Clean ups
        """
        del self.cache
        if self.videoGetter is not None:
            del self.videoGetter

        Log.d("Cleaning up.")
