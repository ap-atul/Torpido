"""
This file is for calculating the textual ranking for the video
,the textual ranking is done by detecting text in the video.
Text detection is achieved by using EAST Text Detection model
of OpenCV, this model can detect text and return confidences and
geometry for the sections that contain the text.
If mixed with text extraction it can give text from the image.
"""

import cv2
import numpy as np

from .config.cache import Cache
from .config.config import Config
from .config.constants import *
from .exceptions import EastModelEnvironmentMissing
from .tools.logger import Log
from .util import image
from .tools.ranking import Ranking


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
    __frame_count : int
        number of frames in the video
    __text_ranks : list
        list of the ranks
    __video_getter : OpenCV
        opencv file reader
    __cache : Cache
        object of the Cache to store the ranking
    __min_confidence : int
        minimum confidence to determine if the video contains text
    __WIDTH : int, default=320
        the east model requires the frame to be size of multiple of 32x32
    __HEIGHT : int, default=320
        height of the frame
    __skip_frames : int
        no of frames to skip
    __net : object
        loaded east model
    __text_detect_layer_name
        layer name to detect the text in the video and return the code
    __text_display_layer_names
        layers to detect and return the coordinates of the boxes of text detected
    """

    def __init__(self):
        cv2.setUseOptimized(True)
        self.__fps = self.__frame_count = self.__text_ranks = self.__video_getter = None
        self.__cache = Cache()
        self.__min_confidence, self.__skip_frames = Config.TEXT_MIN_CONFIDENCE, Config.TEXT_SKIP_FRAMES
        self.__WIDTH = self.__HEIGHT = 320  # same thing for this

        # saving the original dim of the frame
        self._original_H, self._original_W = None, None

        # initializing the model
        # reading the model in the memory
        if TEXT_EAST_MODEL_PATH is not None:
            self.__net = cv2.dnn.readNet(TEXT_EAST_MODEL_PATH)
        else:
            raise EastModelEnvironmentMissing

        # adding output layer to only return confidence for text
        self.__text_detect_layer_name = ["feature_fusion/Conv_7/Sigmoid"]

        # adding output layers to the model with text detected boxes
        self.__text_display_layer_names = ["feature_fusion/Conv_7/Sigmoid",
                                           "feature_fusion/concat_3"]

    def __run_text_detect(self, blob):
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
        scores = self.__net.forward(self.__text_detect_layer_name)
        num_rows, num_cols = np.asarray(scores).shape[3: 5]
        confidences = list()

        # make this faster some how ?
        # since image is 320x320 the output is 80x80 (scores)
        for x in range(0, num_rows):
            score_data = scores[0][0][0][x]
            for y in range(0, num_cols):
                if score_data[y] < self.__min_confidence:
                    continue

                confidences.append(score_data[y])

        # if confidences contain some value
        if len(confidences) > 0:
            return True

        return False

    def __run_text_detect_display(self, blob, original):
        """
        Function to detect text using layer for getting the rectangles
        to display on the frame

        Parameters
        ----------
        blob : blob
            blob of the image
        original : image array
            un-resized image to display

        Returns
        -------
        bool
            True denotes text detected
        """
        # running the model
        self.__net.setInput(blob=blob)
        scores, geometry = self.__net.forward(self.__text_display_layer_names)

        num_rows, num_cols = scores.shape[2:4]
        rW = self._original_W / float(self.__WIDTH)
        rH = self._original_H / float(self.__HEIGHT)
        rSize = (rW, rH)
        rect, confidences = list(), list()

        # since image is 320x320 the output is 80x80 (scores)
        for y in range(0, num_rows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(0, num_cols):
                # if our score does not have sufficient probability, ignore it
                if scoresData[x] < self.__min_confidence:
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
        boxes = image.non_max_suppression(np.array(rect), probs=confidences)

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

    def __timed_ranking_normalize(self):
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
        text_normalize = list()

        if len(self.__text_ranks) == 0:
            text_normalize.extend([0] * int(self.__frame_count))

        for i in range(0, int(self.__frame_count), int(self.__fps)):
            if len(self.__text_ranks) >= (i + int(self.__fps)):
                text_normalize.append(np.mean(self.__text_ranks[i: i + int(self.__fps)]))
            else:
                break

        # saving all processed stuffs
        Ranking.add(CACHE_RANK_TEXT, text_normalize)
        Log.d(f"Textual rank length {len(text_normalize)}")
        Log.i("Textual ranking saved .............")

    def __del__(self):
        """ clean ups """
        del self.__net
        del self.__video_getter
        Log.d("Cleaning up.")

    def start_processing(self, input_file, display=False):
        """
        Function to perform the Textual Processing on the input video file.
        The video can be displayed as the processing is going on.

        Parameters
        ----------
        input_file : str
            input video file
        display : bool
            True to display the video while processing
        """

        if os.path.isfile(input_file) is False:
            Log.e(f"File {input_file} does not exists")
            return

        self.__video_getter = cv2.VideoCapture(str(input_file))
        self.__fps = self.__video_getter.get(cv2.CAP_PROP_FPS)
        self.__frame_count = self.__video_getter.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__skip_frames = int(self.__fps * self.__skip_frames)

        # maintaining the ranks for text detection
        count, original = 0, None
        self.__text_ranks = list()

        while True:
            ret, frame = self.__video_getter.read()

            if frame is None or not ret:
                break

            if self._original_H is None:
                self._original_H, self._original_W = frame.shape[:2]

            if display:
                original = frame

            # resizing the frame to a multiple of 32 x 32
            frame = cv2.resize(frame, (self.__WIDTH, self.__HEIGHT))

            count += 1
            if count % self.__skip_frames == 0:

                #  making the image blob
                blob = cv2.dnn.blobFromImage(frame,
                                             1.0,
                                             (self.__WIDTH, self.__HEIGHT),
                                             (123.68, 116.78, 103.94),
                                             swapRB=True, crop=False)

                # run text detection
                if display:
                    detected_text = self.__run_text_detect_display(blob, original)
                else:
                    detected_text = self.__run_text_detect(blob)

                # if text is detected
                if detected_text:
                    self.__text_ranks.extend([Config.RANK_TEXT] * int(self.__skip_frames))
                    Log.d("Text detected.")
                else:
                    self.__text_ranks.extend([0] * int(self.__skip_frames))
                    Log.d("No text detected.")

        # clearing the memory
        self.__video_getter.release()

        if display:
            cv2.destroyAllWindows()

        # calling the normalization of ranking
        self.__timed_ranking_normalize()
