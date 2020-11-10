"""
This file is for calculating the textual ranking for the video
,the textual ranking is done by detecting text in the video.
Text detection is achieved by using EAST Text Detection model
of OpenCV, this model can detect text and return confidences and
geometry for the sections that contain the text.
If mixed with text extraction it can give text from the image.
"""

import time

import cv2
import numpy as np

from torpido.config import *
from torpido.exceptions import EastModelEnvironmentMissing
from torpido.util import image
from torpido.video import VideoGet


class Textual:
    """
    Class to perform Textual analysis on the input video file. This class creates its own
    video reader and handles the frame independent of the `Visual`. The EAST model of the
    OpenCV is used to detect text in the video.

    Since, the model is very slow depend-ing on the system its running. So some of the frames
    are skipped `TEXT_SKIP_FRAMES` determines the no of frames to skip

    Attributes
    ----------
    __fps : float
        video fps
    __frameCount : int
        number of frames in the video
    __textRanks : list
        list of the ranks
    __videoGetter : VideoGet
        object of the video get to read the video through thread
    __minConfidence : int
        minimum confidence to determine if the video contains text
    __WIDTH : int, default=320
        the east model requires the frame to be size of multiple of 32x32
    __HEIGHT : int, default=320
        height of the frame
    __skipFrames : int
        no of frames to skip
    __textRankPath : str
        constants file defines where to store the ranks
    __net : object
        loaded east model
    __textDetectLayerName
        layer name to detect the text in the video and return the code
    __textDisplayLayerNames
        layers to detect and return the coordinates of the boxes of text detected
    """

    def __init__(self):
        cv2.setUseOptimized(True)
        self.__fps = None
        self.__frameCount = None
        self.__textRanks = None
        self.__videoGetter = None
        self.__minConfidence = TEXT_MIN_CONFIDENCE
        self.__WIDTH = 320  # this val should be multiple of 32
        self.__HEIGHT = 320  # same thing for this
        self.__skipFrames = TEXT_SKIP_FRAMES
        self.__textRankPath = os.path.join(os.getcwd(), RANK_DIR, RANK_OUT_TEXT)

        # initializing the model
        # reading the model in the memory
        if TEXT_EAST_MODEL_PATH is not None:
            self.__net = cv2.dnn.readNet(TEXT_EAST_MODEL_PATH)
        else:
            raise EastModelEnvironmentMissing

        # adding output layer to only return confidence for text
        self.__textDetectLayerName = ["feature_fusion/Conv_7/Sigmoid"]

        # adding output layers to the model with text detected boxes
        self.__textDisplayLayerNames = ["feature_fusion/Conv_7/Sigmoid",
                                        "feature_fusion/concat_3"]

    def startProcessing(self, inputFile, display=False):
        """
        Function to perform the Textual Processing on the input video file.
        The video can be displayed as the processing is going on.

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

        self.__videoGetter = VideoGet(str(inputFile)).start()
        myClip = self.__videoGetter.stream

        if self.__videoGetter.getQueueSize() == 0:
            time.sleep(0.5)
            Log.d("Waiting for the buffer to fill up.")

        self.__fps = myClip.get(cv2.CAP_PROP_FPS)
        self.__frameCount = myClip.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__skipFrames = int(self.__fps * self.__skipFrames)

        # maintaining the ranks for text detection
        count = 0
        self.__textRanks = []

        while self.__videoGetter.more():
            frame = self.__videoGetter.read()

            if frame is None:
                break

            # resizing the frame to a multiple of 32 x 32
            # resizing the frame
            original = frame
            (H, W) = frame.shape[:2]
            rW = W / float(self.__WIDTH)
            rH = H / float(self.__HEIGHT)
            frame = cv2.resize(frame, (W, H))
            count += 1

            if count % self.__skipFrames == 0:
                detectedText = False

                #  making the image blob
                blob = cv2.dnn.blobFromImage(frame,
                                             1.0,
                                             (self.__WIDTH, self.__HEIGHT),
                                             (123.68, 116.78, 103.94),
                                             swapRB=True, crop=False)

                # run text detection
                if display:
                    if self.__runTextDetectDisplay(blob, (rW, rH), original):
                        detectedText = True
                else:
                    if self.__runTextDetect(blob):
                        detectedText = True

                # if text is detected
                if detectedText:
                    self.__textRanks.extend([RANK_TEXT] * int(self.__skipFrames))
                    Log.d("Text detected.")
                else:
                    self.__textRanks.extend([0] * int(self.__skipFrames))
                    Log.d("No text detected.")

        # clearing the memory
        myClip.release()
        self.__videoGetter.stop()
        cv2.destroyAllWindows()

        # calling the normalization of ranking
        self.__timedRankingNormalize()

    def __runTextDetect(self, blob):
        """
        Function to detect only text and no display. Gets the scores and calculates if the image
        contains any text

        Parameters
        ----------
        blob : blob
            blob of the image

        Returns
        -------
        bool
            True denotes text detected
        """
        self.__net.setInput(blob)
        scores = self.__net.forward(self.__textDetectLayerName)
        numRows, numCols = np.asarray(scores).shape[3: 5]
        confidences = []

        # since image is 320x320 the output is 80x80 (scores)
        for x in range(0, numRows):
            scoreData = scores[0][0][0][x]
            for y in range(0, numCols):
                if scoreData[y] < self.__minConfidence:
                    continue

                confidences.append(scoreData[y])

        # if confidences contain some value
        if len(confidences) > 1:
            return True
        return False

    def __runTextDetectDisplay(self, blob, rSize, original):
        """
        Function to detect text using layer for getting the rectangles
        to display on the frame

        Parameters
        ----------
        blob : blob
            blob of the image
        rSize : tuple
            real sizes of the images
        original : image array
            un-resized image to display

        Returns
        -------
        bool
            True denotes text detected
        """
        # running the model
        self.__net.setInput(blob=blob)
        scores, geometry = self.__net.forward(self.__textDisplayLayerNames)

        numRows, numCols = scores.shape[2:4]
        rect = []
        confidences = []

        # since image is 320x320 the output is 80x80 (scores)
        for y in range(0, numRows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(0, numCols):
                # if our score does not have sufficient probability, ignore it
                if scoresData[x] < self.__minConfidence:
                    continue

                # compute the offset factor as our resulting feature maps will
                # be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4, y * 4)

                # extract the rotation angle for the prediction and then
                # compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height of
                # the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates for
                # the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score to
                # our respective lists
                rect.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        # compressing the boxes or rectangles
        boxes = image.nonMaxSuppression(np.array(rect), probs=confidences)

        rW, rH = rSize
        for startX, startY, endX, endY in boxes:
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            # draw the bounding box on the image
            cv2.rectangle(original, (startX, startY), (endX, endY), (0, 255, 0), 2)

        cv2.imshow("Text Detection", original)
        cv2.waitKey(1) & 0xFF

        if len(confidences) > 0:
            return True
        return False

    def __timedRankingNormalize(self):
        """
        Since ranking is added to frames, since frames are duration * fps
        and audio frame system is different since frame are duration * rate
        so we need to generalize the ranking system

        sol: ranking sec of the video and audio, for than taking mean of the
        frames to generate rank for video.
        since ranking is 0 or 1, the mean will be different and we get more versatile
        results.

        we will read the list and slice the video to get 1 sec of frames and get
        mean/average as the rank for the 1 sec
        """
        textNormalize = []
        for i in range(0, int(self.__frameCount), int(self.__fps)):
            if len(self.__textRanks) >= (i + int(self.__fps)):
                textNormalize.append(np.mean(self.__textRanks[i: i + int(self.__fps)]))
            else:
                break

        # saving all processed stuffs
        dump(textNormalize, self.__textRankPath)
        Log.d(f"Textual rank length {len(textNormalize)}")
        Log.i("Textual ranking saved .............")

    def __del__(self):
        """
        clean ups
        """
        del self.__net
        del self.__videoGetter
        Log.d("Cleaning up.")
