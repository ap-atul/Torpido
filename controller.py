import gc
import os
from multiprocessing import Process

from lib.auditory import Auditory
from lib.io import FFMPEG
from lib.textual import Textual
from lib.util.cache import Cache
from lib.util.timestampTool import getTimestamps
from lib.util.validate import checkIfVideo
from lib.visual import Visual

print("""\033[93m

___________                 .__    .___
\__    ___/________________ |__| __| _/____
  |    | /  _ \_  __ \____ \|  |/ __ |/  _ \
  |    |(  <_> )  | \/  |_> >  / /_/ (  <_> )
  |____| \____/|__|  |   __/|__\____ |\____/
                     |__|           \/
                \033[37;41m Video editing made fun ;) \033[0m
_______________________________________________

""")
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
            print(f"[ERROR] Video file does not exists.")
            return

        if not checkIfVideo(inputFile):
            return

        if self.ffmpeg.splitVideoAudio(inputFile):
            print("[INFO] Splitting the file")

        self.videoFile = inputFile
        self.outputFile = self.ffmpeg.getOutputFileNamePath()
        self.audioFile = self.ffmpeg.getInputAudioFileNamePath()

        # starting the sub processes
        self.startModules(display)

    def startModules(self, display):
        """
        creating multiple processes for each work load
        each of them is independent and share nothing
        :param display: bool, plotting and video play
        :return: None
        """
        audioProcess = Process(target=self.auditory.startProcessing, args=(self.audioFile, display))
        visualProcess = Process(target=self.visual.startProcessing, args=(self.videoFile, display))
        textualProcess = Process(target=self.textual.startProcessing, args=(self.videoFile, display))

        audioProcess.start()
        visualProcess.start()
        textualProcess.start()

        audioProcess.join()
        visualProcess.join()
        textualProcess.join()

        print(f"[INFO] Garbage collecting .. {gc.collect()}")
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
            print("[INFO] There are not good enough portions to cut. Try changing the config")
            return

        if self.ffmpeg.mergeAudioVideo(timestamps):
            print("Merging the final output video ...............")

        self.ffmpeg.cleanUp()


control = Controller()
control.startProcessing("examples/output/example_01.mp4", True)
