import os

import cv2
import imutils
import numpy as np
from joblib import dump

from lib.util.constants import *
from lib.util.videoReader import VideoGet

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
        self.fps = None
        self.frameCount = None
        self.motion = None
        self.blur = None

    def detectBlur(self, image):
        """
        Laplacian take 2nd derivative of one channel of the image(gray scale)
        It highlights regions of an image containing rapid intensity changes, much like the Sobel and Scharr operators.
        And then calculates the variance (squared SD), then check if the variance satisfies the Threshold value/

        :param image: input image array
        :return: true / false blur (opposite : returns true(1) if image is not blur)
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
        file to run the motion detection and blur detection
        :param display: display the video while processing
        :param inputFile: input file path
        :return: None
        """
        if os.path.isfile(inputFile) is False:
            print(f"[ERROR] File {inputFile} does not exists")
            return

        videoWidth = VIDEO_WIDTH

        # maintaining the motion and blur frames list
        self.motion = list()
        self.blur = list()

        videoGetter = VideoGet(str(inputFile)).start()
        myClip = videoGetter.stream

        fps = myClip.get(cv2.CAP_PROP_FPS)
        totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)

        self.fps = fps
        self.frameCount = totalFrames

        # printing some info
        print("[INFO] Total count of video frames ::", totalFrames)
        print("[INFO] Video fps ::", fps)
        print("[INFO] Bit rate ::", cv2.CAP_PROP_BITRATE)
        print("[INFO] Video format ::", cv2.CAP_PROP_FORMAT)
        print("[INFO] Video four cc :: ", cv2.CAP_PROP_FOURCC)

        threshold = float(MOTION_THRESHOLD)
        np.seterr(divide='ignore')

        firstFrame = videoGetter.frame
        firstFrameProcessed = True

        while True:
            if videoGetter.stopped:
                videoGetter.stop()
                break

            frame = videoGetter.frame

            if frame is None:
                break

            frame = imutils.resize(frame, width=videoWidth)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.blur.append(self.detectBlur(frame))
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
                self.motion.append(RANK_MOTION)
            else:
                self.motion.append(0)

            if display:
                cv2.imshow("Video Feed", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key is pressed, break from the loop
                if key == ord("q"):
                    break

            # assigning the processed frame as the first frame to cal diff later on
            firstFrame = frame

        # clearing memory
        myClip.release()
        videoGetter.stop()
        cv2.destroyAllWindows()

        # calling the normalization of ranking
        self.timedRankingNormalize()

    def timedRankingNormalize(self):
        """
        since ranking is added to frames, since frames are duration * fps
        and audio frame system is different since frame are duration * rate
        so we need to generalize the ranking system
        sol: ranking sec of the video and audio, for than taking mean of the
        frames to generate rank for video.
        since ranking is 0 or 1, the mean will be different and we get more versatile
        results.

        we will read both the list and slice the video to get 1 sec of frames(1 * fps) and get
        mean/average as the rank for the 1 sec
        :return: None
        """
        motionNormalize = []
        blurNormalize = []
        for i in range(0, int(self.frameCount), int(self.fps)):
            if (i + int(self.fps)) < int(self.frameCount):
                motionNormalize.append(np.mean(self.motion[i: i + int(self.fps)]))
                blurNormalize.append(np.mean(self.blur[i: i + int(self.fps)]))

        # saving all processed stuffs
        dump(motionNormalize, self.motionRankPath)
        dump(blurNormalize, self.blurRankPath)
        print(f"[INFO] Visual rank length {len(motionNormalize)}  {len(blurNormalize)}")
        print("[INFO] Visual ranking saved .............")
