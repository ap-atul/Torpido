"""
Controller class will control all the functions to perform
it will link all the libs together and work each process by process
Since, threads and processes need to communicate, the controller
object would be shared in functions
"""

import gc
import os
import time
from multiprocessing import Process, Pipe, Queue
from threading import Thread

from torpido import Auditory, FFMPEG, Textual, Visual
from torpido.analytics import Analytics
from torpido.config import Cache
from torpido.exceptions import RankingOfFeatureMissing, EastModelEnvironmentMissing
from torpido.tools import Watcher, Log
from torpido.util import checkIfVideo, getTimestamps, getOutputVideoLength, readTheRankings


def logo():
    print("""\033[93m
      _                   _     _       
     | |_ ___  _ __ _ __ (_) __| | ___  
     | __/ _ \| '__| '_ \| |/ _` |/ _ \ 
     | || (_) | |  | |_) | | (_| | (_) |
      \__\___/|_|  | .__/|_|\__,_|\___/ 
                   |_|                  
    
             \033[37;41m Video editing made fun ;) \033[0m
    ________________________________________
    
    """)

    time.sleep(1)


class Controller:
    """
    Main bridge between the UI and all the modules exists for the job.
    Following the MVC architecture.

    Inheriting from the QPySignal to create signal slots to display texts
    and to make the working of the UI not blocking

    Attributes
    ----------
    __App : ui controller
        middleware of the controller and the ui
    __videoFile : str
        input video file to process
    __outputFile : str
        output video file generated
    __audioFile : str
        input audio file split from the video file
    __audioProcess : Process
        process to perform audio processing
    __visualProcess : Process
        process to perform video processing
    __textualProcess : Process
        process to perform video text detection
    __deNoisedAudioFile : str
        output audio file from the audio processing
    __videoDisplay : bool
        displays the output video
    __textDetectDisplay : bool
        displays the output video when text is detected
    __snrPlotDisplay : bool
        displays the snr plot for the audio
    __analyticsDisplay : bool
        displays the analytics of the processing
    __visual : Visual
        object of the video processing class
    __auditory : Auditory
        object of the audio processing class
    __textual : Textual
        object of the text video processing class
    __ffmpeg : FFMPEG
        object of the ffmpeg class to perform io operations
    __analytics : Analytics
        object of the class to perform analytics on the processes
    __cache : Cache
        object of the cache class to store the cache
    __watcher : Watcher
        object of the class watcher that monitors cpu and ram usage
    __progressParentPipe : link
        parent communication pipe for the progress bar
    __progressChildPipe : link
        child communication pipe for the progress bar
    __loggerPipe : link / queue
        communication link between the logs and the ui
    __videoPipe : link
        communication pipe for the video display in the gui thread
    """

    def __init__(self):
        self.__App = None
        self.__videoFile = None
        self.__outputFile = None
        self.__audioFile = None
        self.__audioProcess = None
        self.__visualProcess = None
        self.__textualProcess = None
        self.__deNoisedAudioFile = None
        self.__videoDisplay = False
        self.__textDetectDisplay = False
        self.__snrPlotDisplay = False
        self.__analyticsDisplay = False
        self.__visual = Visual()
        self.__auditory = Auditory()
        self.__ffmpeg = FFMPEG()
        self.__analytics = Analytics()
        self.__cache = Cache()
        self.__watcher = Watcher()

        # checking for EAST MODEL env var
        try:
            self.__textual = Textual()
        except EastModelEnvironmentMissing:
            Log.e(EastModelEnvironmentMissing.cause)
            return

        # communication links
        self.__progressParentPipe, self.__progressChildPipe = None, None
        self.__loggerPipe = Queue()
        self.__videoPipe = None

        # communication for logs to ui
        Log.setHandler(self.__loggerPipe)

        # watcher enable/disable
        self.__watcher.enable(self, enable=True)

    def startProcessing(self, app, inputFile):
        """
        Process the input file call splitting function to split the input video file into
        audio and create 3 processes each for feature ranking, After completion of all the
        processes (waiting). Call the completed process method the start the timestamp
        extraction from the ranks

        Parameters
        ----------
        app : some controller object
            handles ui interactions
        inputFile : str
            input video file (validating if its in supported format)

        Notes
        ------
        Using Multi-processing instead of Multi-threading to avoid resources sharing,
        resources like Queue that is used to reading the video using Thread. Threads
        shared the Queue and caused skipping of lots of frames and messing with the
        ranking system completely.

        Difference between Threading and Processing

            - Threading share data and variables without asking
            - Processing won't to that unless told so

        """
        logo()

        # saving the instance of the ui controller
        self.__App = app

        # creating pipe for progress bar communication
        self.__progressParentPipe, self.__progressChildPipe = Pipe()

        # starting listening on the communication link
        Thread(target=self.setPercent, args=()).start()
        Thread(target=self.setLog, args=()).start()

        # initialize the queue and thread
        if self.__videoDisplay:
            self.__videoPipe = Queue()
            self.__visual.setPipe(self.__videoPipe)
            Thread(target=self.setVideo, args=()).start()

        # if from terminal
        if self.__App is None:
            self.__textDetectDisplay = True

        if not os.path.isfile(inputFile):
            Log.e(f"Video file does not exists.")
            return

        if not checkIfVideo(inputFile):
            return

        if self.__ffmpeg.splitVideoAudio(inputFile):
            Log.d("The input video has been split successfully")
        # something went wrong [mostly video does not contain any audio]
        else:
            Log.e("Logging out")
            return

        self.__videoFile = inputFile
        self.__outputFile = self.__ffmpeg.getOutputFileNamePath()
        self.__audioFile = self.__ffmpeg.getInputAudioFileNamePath()
        self.__deNoisedAudioFile = self.__ffmpeg.getOutputAudioFileNamePath()

        # starting the sub processes
        self.__startModules()

    def __startModules(self):
        """
        Creating 3 processes using the Process class of the multi-processing module.
        FFmpeg separated files are referenced from the Controller public variables
        """
        self.__watcher.start()  # starting the watcher

        self.__audioProcess = Process(target=self.__auditory.startProcessing,
                                      args=(self.__audioFile,
                                            self.__deNoisedAudioFile,
                                            self.__snrPlotDisplay))

        self.__visualProcess = Process(target=self.__visual.startProcessing,
                                       args=(self.__progressChildPipe,
                                             self.__videoFile,
                                             self.__videoDisplay))

        self.__textualProcess = Process(target=self.__textual.startProcessing,
                                        args=(self.__videoFile,
                                              self.__textDetectDisplay))

        self.__audioProcess.start()
        self.__visualProcess.start()
        self.__textualProcess.start()

        self.__audioProcess.join()
        self.__visualProcess.join()
        self.__textualProcess.join()

        # running the final pass
        Log.d(f"Garbage collecting .. {gc.collect()}")
        self.__completedProcess()

    def __completedProcess(self):
        """
        Calls the merging function to merge the processed audio and the input
        video file. Once completed final video is outputted and the audio files
        generated are deleted as a part of the clean up process. Along with it
        the garbage collection module does some clean ups too.
        """
        self.__watcher.end()  # ending the watcher
        data = readTheRankings()

        if self.__analyticsDisplay:
            #  separate process for analytics
            Process(target=self.__analytics.analyze, args=(data,)).start()

        try:
            timestamps = getTimestamps(data=data)
        except RankingOfFeatureMissing:
            Log.e(RankingOfFeatureMissing.cause)
            return

        if len(timestamps) == 0:
            Log.w("There are not good enough portions to cut. Try changing the configurations.")
            return

        Log.i(f"Clipping a total of {len(timestamps)} sub portions.")
        Log.i(f"Output video length would be approx. :: {getOutputVideoLength(timestamps)}")
        if self.__ffmpeg.mergeAudioVideo(timestamps):
            Log.d("Merged the final output video ...............")
        else:
            return

    def __del__(self):
        """clean up"""
        if self.__visualProcess is not None:
            self.__visualProcess.terminate()
        if self.__audioProcess is not None:
            self.__audioProcess.terminate()
        if self.__textualProcess is not None:
            self.__textualProcess.terminate()
        if self.__progressParentPipe is not None:
            self.__progressParentPipe.close()
        if self.__progressChildPipe is not None:
            self.__progressChildPipe.close()

        # deleting files created by processing modules
        self.__ffmpeg.cleanUp()
        Log.d("Terminating the processes")

    def __closeCommunication(self):
        """ Close all the pipes """
        if self.__progressParentPipe is not None:
            self.__progressParentPipe.close()
        if self.__progressChildPipe is not None:
            self.__progressChildPipe.close()

    def setSaveLogs(self, value=False):
        """ Save all the logs to a file """
        Log.toFile = value

    def setVideoDisplay(self, value=False):
        """ Display the processing video output """
        self.__videoDisplay = value

    def setSNRPlot(self, value=False):
        """ Display the snr plot for the audio """
        self.__snrPlotDisplay = value

    def setRankingPlot(self, value=False):
        """ Display the analytics """
        self.__analyticsDisplay = value

    def setPercent(self):
        """ Send the signal to the ui with the percentage of processing """
        while True:
            value = self.__progressParentPipe.recv()

            # checking whether the request is from UI
            if self.__App is not None and value is not None:
                self.__App.setPercentComplete(value)

                if value == 100:
                    self.__App.setVideoClose()
                    self.__closeCommunication()
                    break

    def setLog(self):
        """ Send the signal to the ui with the log of the processing """
        while True:
            try:
                message = self.__loggerPipe.get()

                # checking whether the request is from UI
                if self.__App is not None and message is not None:
                    self.__App.setMessageLog(message)
            except EOFError as _:
                pass

    def setVideo(self):
        """ Send the signal to the ui with the vidoe frame to display """
        while True:
            try:
                frame = self.__videoPipe.get()

                # checking whether the request is from UI
                if self.__App is not None and frame is not None:
                    self.__App.setVideoFrame(frame)
            except EOFError as _:
                pass

    def setCpuComplete(self, val):
        """ Send the signal to the ui with the percent usage of the cpu """
        # checking whether the request is from UI
        if self.__App is not None:
            self.__App.setCpuComplete(val)

    def setMemComplete(self, val):
        """ Send the signal to the ui with the percent usage of the ram/memory """
        # checking whether the request is from UI
        if self.__App is not None:
            self.__App.setMemComplete(val)
