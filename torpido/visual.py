"""
This file reads the video and gives ranking to frames
that have motion in it, saves in the dictionary with frame numbers
this dictionary is then saved in a joblib file defined in constants.py
"""

from time import sleep

import cv2
import numpy as np

from .config.config import Config
from torpido.config.cache import Cache
from torpido.config.constants import *
from torpido.tools.logger import Log
from torpido.video import VideoGet


class Visual:
    """
    Class to perform Visual Processing on the input video file. Motion and Blur detections
    are used to calculate the rank. The ranks are per frame, so later the ranks are
    normalized to sec

    Attributes
    ----------
    self.__blur_threshold : int
        threshold to rank the blur feature
    self.__motion_threshold : int
        threshold to rank the motion feature
    self.__fps : float
        input video fps
    self.__frame_count : int
        number of frames
    self.__motion : list
        list of the ranks for the motion feature
    self.__blur : list
        list of the ranks for the blur feature
    self.__cache : Cache
        cache object to store the data
    self.__video_getter : VideoGet
        video reader object to read the video and save it in thread
    """

    def __init__(self):
        cv2.setUseOptimized(True)
        self.__blur_threshold = Config.BLUR_THRESHOLD
        self.__motion_threshold = Config.MOTION_THRESHOLD
        self.__cache = Cache()
        self.__fps = None
        self.__frame_count = None
        self.__motion = None
        self.__blur = None
        self.__video_getter = None
        self.__video_pipe = None

    def __detect_blur(self, image):
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
        if cv2.Laplacian(image, cv2.CV_64F).var() >= self.__blur_threshold:
            return 0
        return Config.RANK_BLUR

    def __timed_ranking_normalize(self):
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
        motion_normalize = list()
        blur_normalize = list()
        for i in range(0, int(self.__frame_count), int(self.__fps)):
            if len(self.__motion) >= (i + int(self.__fps)):
                motion_normalize.append(np.mean(self.__motion[i: i + int(self.__fps)]))
                blur_normalize.append(np.mean(self.__blur[i: i + int(self.__fps)]))
            else:
                break

        # saving all processed stuffs
        self.__cache.write_data(CACHE_RANK_MOTION, motion_normalize)
        self.__cache.write_data(CACHE_RANK_BLUR, blur_normalize)
        Log.d(f"Visual rank length {len(motion_normalize)}  {len(blur_normalize)}")
        Log.i(f"Visual ranking saved .............")

    def __set_video_fps(self):
        """ Function to set the original video fps to cache """
        self.__cache.write_data(CACHE_FPS, self.__fps)

    def __set_video_frame_count(self):
        """ Function to set the original video frame count to cache """
        self.__cache.write_data(CACHE_FRAME_COUNT, self.__frame_count)

    def __del__(self):
        """ Clean  ups """
        del self.__cache
        if self.__video_getter is not None:
            del self.__video_getter

        Log.d("Cleaning up.")

    def start_processing(self, pipe, inputFile, display=False):
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
        self.__motion, self.__blur = list(), list()

        self.__video_getter = VideoGet(str(inputFile)).start()
        my_clip = self.__video_getter.stream

        if self.__video_getter.get_queue_size() == 0:
            sleep(1)
            Log.d(f"Waiting for the buffer to fill up.")

        fps = my_clip.get(cv2.CAP_PROP_FPS)
        total_frames = my_clip.get(cv2.CAP_PROP_FRAME_COUNT)

        self.__fps = fps
        self.__frame_count = total_frames
        self.__set_video_fps()
        self.__set_video_frame_count()
        self.__cache.write_data(CACHE_VIDEO_WIDTH, cv2.CAP_PROP_FRAME_WIDTH)
        self.__cache.write_data(CACHE_VIDEO_HEIGHT, cv2.CAP_PROP_FRAME_HEIGHT)

        # printing some info
        Log.d(f"Total count of video frames :: {total_frames}")
        Log.i(f"Video fps :: {fps}")
        Log.i(f"Bit rate :: {cv2.CAP_PROP_BITRATE}")
        Log.i(f"Video format :: {cv2.CAP_PROP_FORMAT}")
        Log.i(f"Video four cc :: {cv2.CAP_PROP_FOURCC}")

        count = 0
        first_frame = self.__video_getter.read()
        first_frame_processed = True
        original = None

        while self.__video_getter.more():
            frame = self.__video_getter.read()

            if frame is None:
                break

            if display:
                original = frame

            count += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.__blur.append(self.__detect_blur(frame))
            frame = cv2.GaussianBlur(frame, (21, 21), 0)

            if first_frame_processed:
                first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
                first_frame = cv2.GaussianBlur(first_frame, (21, 21), 0)
                first_frame_processed = False

            frameDelta = cv2.absdiff(first_frame, frame)
            thresh = cv2.threshold(frameDelta, self.__motion_threshold, 255, cv2.THRESH_BINARY)[1]

            threshMax = np.max(thresh)
            if threshMax > 0:
                self.__motion.append(Config.RANK_MOTION)
            else:
                self.__motion.append(0)

            if display:

                # adding the frame to the pipe
                if self.__video_pipe is not None:
                    self.__video_pipe.send(ID_COM_VIDEO, original)

                # not a ui request, so this works
                else:
                    cv2.imshow("Video Output", original)
                    # if the `q` key is pressed, break from the loop

            # assigning the processed frame as the first frame to cal diff later on
            first_frame = frame

            # setting progress on the ui
            if pipe is not None:
                pipe.send(ID_COM_PROGRESS, float((count / total_frames) * 100))

        # completing the progress
        if pipe is not None:
            pipe.send(ID_COM_PROGRESS, 99.0)

        # clearing memory
        my_clip.release()
        self.__video_getter.stop()

        # calling the normalization of ranking
        self.__timed_ranking_normalize()

    def set_pipe(self, pipe):
        """
        Send video frame to the ui threads for displaying, since open cv
        is using the Qt backend, it should be in the main ui thread or else
        the im show does not work in the sub process

        Parameters
        ----------
        pipe : some queue
            add frames and continuous read to the ui display
        """
        self.__video_pipe = pipe
