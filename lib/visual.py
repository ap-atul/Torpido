import os

import cv2
import imutils
import numpy as np
from joblib import dump

from lib.util.constants import *
from lib.util.video_reader import VideoGet

"""
This file reads the video and gives ranking to frames
that have motion in it, saves in the dictionary with frame numbers
this dictionary is then saved in a joblib file defined in constants.py
"""


class Visual:
    def __init__(self):
        self.motionRankPath = os.path.join(RANK_DIR, RANK_OUT_MOTION)
        self.blurRankPath = os.path.join(RANK_DIR, RANK_OUT_BLUR)
        self.blurThreshold = BLUR_THRESHOLD

    def detectBlur(self, image):
        """
        Laplacian take 2nd derivative of one channel of the image(gray scale)
        It highlights regions of an image containing rapid intensity changes, much like the Sobel and Scharr operators.
        And then calculates the variance (squared SD), then check if the variance satisfies the Threshold value/

        :param image: input image array
        :return: true / false blur (opposite : returns true if image is not blur)
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
        return cv2.Laplacian(image, cv2.CV_64F).var() >= self.blurThreshold

    def startProcessing(self, inputFile):
        """
        file to run the motion detection and blur detection
        :param inputFile: input file path
        :return: None
        """
        videoWidth = VIDEO_WIDTH

        # maintaining the motion frames list
        motion = dict()
        blur = dict()

        video_getter = VideoGet(str(inputFile)).start()
        myClip = video_getter.stream

        fps = myClip.get(cv2.CAP_PROP_FPS)
        totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)
        print("TotalFrames ::", totalFrames)
        print("Video FPS ::", fps)

        threshold = float(MOTION_THRESHOLD)
        np.seterr(divide='ignore')

        firstFrame = video_getter.frame
        firstFrameProcessed = True

        while True:
            if video_getter.stopped:
                video_getter.stop()
                break

            frameIndex = myClip.get(cv2.CAP_PROP_POS_FRAMES)
            frame = video_getter.frame

            if frame is None:
                break

            frame = imutils.resize(frame, width=videoWidth)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            val = self.detectBlur(frame)
            blur[frameIndex] = int(val)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)

            if firstFrameProcessed:
                firstFrame = imutils.resize(firstFrame, width=videoWidth)
                firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
                firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
                firstFrameProcessed = False

            frameDelta = cv2.absdiff(firstFrame, frame)
            thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]

            threshSum = thresh.sum()
            if threshSum > 0:
                motion[frameIndex] = 1
            else:
                motion[frameIndex] = 0

            cv2.imshow("Security Feed", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key is pressed, break from the loop
            if key == ord("q"):
                break

            # assigning the processed frame as the first frame to cal diff later on
            firstFrame = frame

        # saving all processed stuffs
        dump(motion, self.motionRankPath)
        dump(blur, self.blurRankPath)

        # clearing memory
        myClip.release()
        cv2.destroyAllWindows()
