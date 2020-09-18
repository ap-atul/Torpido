import gc
import os
import time
from multiprocessing import Process

from lib.auditory import Auditory
from lib.io import FFMPEG
from lib.textual import Textual
from lib.util.cache import Cache
from lib.util.logger import Log
from lib.util.timestampTool import getTimestamps
from lib.util.validate import checkIfVideo
from lib.visual import Visual

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
"""
Controller class will control all the functions to perform
it will link all the libs together and work each process by process
Since, threads and processes need to communicate, the controller 
object would be shared in functions
"""


class Controller:
    def __init__(self):
        self.fps = None
        self.videoFile = None
        self.outputFile = None
        self.audioFile = None
        self.deNoisedAudioFile = None
        self.audioProcess = None
        self.visualProcess = None
        self.textualProcess = None
        self.visual = Visual()
        self.auditory = Auditory()
        self.textual = Textual()
        self.ffmpeg = FFMPEG()
        self.cache = Cache()

    def startProcessing(self, inputFile, display=False):
        """
        starting the main processed on the input video file,
        this function will launch sub processes that does the main
        rank
        Shifted from Threading to Processing ------------------
        :param inputFile: str, input video file
        :param display: bool, display video and audio plots
        :return: None
        """
        if not os.path.isfile(inputFile):
            Log.e(f"Video file does not exists.")
            return

        if not checkIfVideo(inputFile):
            return

        if self.ffmpeg.splitVideoAudio(inputFile):
            pass

        self.videoFile = inputFile
        self.outputFile = self.ffmpeg.getOutputFileNamePath()
        self.audioFile = self.ffmpeg.getInputAudioFileNamePath()
        self.deNoisedAudioFile = self.ffmpeg.getOutputAudioFileNamePath()

        # starting the sub processes
        self.startModules(display)

    def startModules(self, display):
        """
        creating multiple processes for each work load
        each of them is independent and share nothing
        :param display: bool, plotting and video play
        :return: None
        """
        self.audioProcess = Process(target=self.auditory.startProcessing, args=(self.audioFile, self.deNoisedAudioFile))
        self.visualProcess = Process(target=self.visual.startProcessing, args=(self.videoFile, display))
        # self.textualProcess = Process(target=self.textual.startProcessing, args=(self.videoFile, display))

        self.audioProcess.start()
        self.visualProcess.start()
        # self.textualProcess.start()

        self.audioProcess.join()
        self.visualProcess.join()
        # self.textualProcess.join()

        Log.d(f"Garbage collecting .. {gc.collect()}")
        self.completedProcess()

    def completedProcess(self):
        """
        final merging on the processed video and audio files
        the names are generated programmatically, so only thing
        input is the timestamps (clip time stamps)
        :return: None
        """
        timestamps = getTimestamps()
        if len(timestamps) == 0:
            Log.w("There are not good enough portions to cut. Try changing the config")
            return

        if self.ffmpeg.mergeAudioVideo(timestamps):
            Log.d("Merged the final output video ...............")

        self.ffmpeg.cleanUp()

    def __del__(self):
        if self.visualProcess is not None:
            self.visualProcess.terminate()
        if self.audioProcess is not None:
            self.audioProcess.terminate()
        if self.textualProcess is not None:
            self.textualProcess.terminate()
        Log.d("Terminating the processes")


def call():
    # objgraph.show_growth(limit=5)
    control = Controller()
    # import tracemalloc
    # tracemalloc.start()
    # print(" ************** GETTING GRAPH DATA *********")
    # print(objgraph.show_growth(limit=5))
    # snapshot1 = tracemalloc.take_snapshot()
    control.startProcessing("/home/atul/Videos/testNow/Gretel.mkv", True)
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


call()
