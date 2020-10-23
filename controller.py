"""
Controller class will control all the functions to perform
it will link all the libs together and work each process by process
Since, threads and processes need to communicate, the controller
object would be shared in functions
"""

import gc
import os
import time
from multiprocessing import Process

from lib.auditory import Auditory
from lib.exceptions.custom import RankingOfFeatureMissing, EastModelEnvironmentMissing
from lib.io import FFMPEG
from lib.textual import Textual
from lib.util.cache import Cache
from lib.util.logger import Log
from lib.util.timestamp import getTimestamps, getOutputVideoLength
from lib.util.validate import checkIfVideo
from lib.util.watcher import Watcher
from lib.visual import Visual


def logo():
    print("""\033[93m
      _                   _     _       
     | |_ ___  _ __ _ __ (_) __| | ___  
     | __/ _ \| '__| '_ \| |/ _` |/ _ \ 
     | || (_) | |  | |_) | | (_| | (_) |
      \__\___/|_|  | .__/|_|\__,_|\___/ 
                   |_|                  
    
             \033[37;41m Video editing made fun ;) \033[0m
    _______________________________________________
    
    """)

    time.sleep(1)


class Controller:
    """
    Main bridge between the UI and all the modules exists for the job.
    Following the MVC architecture.

    Inheriting from the QPySignal to create signal slots to display texts
    and to make the working of the UI not blocking
    """

    def __init__(self):
        self.__fps = None
        self.__videoFile = None
        self.__outputFile = None
        self.__audioFile = None
        self.__deNoisedAudioFile = None
        self.__audioProcess = None
        self.__visualProcess = None
        self.__textualProcess = None
        self.__visual = Visual()
        self.__auditory = Auditory()
        self.__ffmpeg = FFMPEG()
        self.__cache = Cache()
        self.__watcher = Watcher()

        # not enables currently
        self.__watcher.enable(False)

        # checking for EAST MODEL env var
        try:
            self.__textual = Textual()
        except EastModelEnvironmentMissing:
            Log.e(EastModelEnvironmentMissing.cause)
            return

    def startProcessing(self, inputFile, display=False):
        """
        Process the input file call splitting function to split the input video file into
        audio and create 3 processes each for feature ranking, After completion of all the
        processes (waiting). Call the completed process method the start the timestamp
        extraction from the ranks

        Parameters
        ----------
        inputFile : str
            input video file (validating if its in supported format)
        display : bool
            True to display the video while processing

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
        self.__startModules(display)

    def __startModules(self, display):
        """
        Creating 3 processes using the Process class of the multi-processing module.
        FFmpeg separated files are referenced from the Controller public variables

        Introducing private vars soon.

        Parameters
        ----------
        display : bool
            to display the video while processing

        """
        self.__watcher.start()  # starting the watcher

        self.__audioProcess = Process(target=self.__auditory.startProcessing,
                                      args=(self.__audioFile, self.__deNoisedAudioFile))
        self.__visualProcess = Process(target=self.__visual.startProcessing, args=(self.__videoFile, display))
        self.__textualProcess = Process(target=self.__textual.startProcessing, args=(self.__videoFile, display))

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

        try:
            timestamps = getTimestamps()
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

        # deleting files created by processing modules
        self.__ffmpeg.cleanUp()
        Log.d("Terminating the processes")


def call():
    print("Calling this")
    # objgraph.show_growth(limit=5)
    control = Controller()
    # import tracemalloc
    # tracemalloc.start()
    # print(" ************** GETTING GRAPH DATA *********")
    # print(objgraph.show_growth(limit=5))
    # snapshot1 = tracemalloc.take_snapshot()
    control.startProcessing("", True)
    # snapshot2 = tracemalloc.take_snapshot()
    # def run_objgraph(type):
    #     objgraph.show_backrefs(type,max_depth=20,
    #          filename='/home/atul/Desktop/graphs/backrefs_%s_%d.png' % (type, os.getpid()))
    #     roots = objgraph.get_leaking_objects()
    #     print("************** LEAKING *****************")
    #     print(objgraph.show_most_common_types(objects=roots))
    #     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #     objgraph.show_refs(roots[:3], refcounts=True,
    #     	filename='/home/atul/Desktop/graphs/leaking_backrefs_%s_%d.png' % (type, os.getpid()))

    # run_objgraph('dict')
    # top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    # print("[ Top 10 differences ]")
    # for stat in top_stats[:10]:
    #     print(stat)

# call()
