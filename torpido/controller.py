"""
Controller class will control all the functions to perform
it will link all the libs together and work each process by process
Since, threads and processes need to communicate, the controller
object would be shared in functions
"""

import gc
import os
from multiprocessing import Process, Pipe, Queue
from threading import Thread
from time import sleep

from torpido import Analytics
from torpido import Auditory, FFMPEG, Textual, Visual
from torpido.config import Cache, LINUX
from torpido.exceptions import RankingOfFeatureMissing, EastModelEnvironmentMissing
from torpido.manager import ManagerPool
from torpido.tools import Watcher, Log
from torpido.util import get_timestamps, read_rankings, check_type_video


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
    __video_file : str
        input video file to process
    __output_file : str
        output video file generated
    __audio_file : str
        input audio file split from the video file
    __audio_process : Process
        process to perform audio processing
    __visual_process : Process
        process to perform video processing
    __textual_process : Process
        process to perform video text detection
    __de_noised_audio_file : str
        output audio file from the audio processing
    __video_display : bool
        displays the output video
    __text_detect_display : bool
        displays the output video when text is detected
    __snr_plot_display : bool
        displays the snr plot for the audio
    __analytics_display : bool
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
    __pool : ManagerPool
        object of the class ManagerPool that sets nice value for the processes
    __progress_parent_pipe : link
        parent communication pipe for the progress bar
    __progress_child_pipe : link
        child communication pipe for the progress bar
    __logger_pipe : link / queue
        communication link between the logs and the ui
    __video_pipe : link
        communication pipe for the video display in the gui thread
    """

    def __init__(self):
        self.__App = None
        self.__video_file = None
        self.__output_file = None
        self.__audio_file = None
        self.__audio_process = None
        self.__visual_process = None
        self.__textual_process = None
        self.__de_noised_audio_file = None
        self.__video_display = False
        self.__text_detect_display = False
        self.__snr_plot_display = False
        self.__analytics_display = False
        self.__visual = Visual()
        self.__auditory = Auditory()
        self.__ffmpeg = FFMPEG()
        self.__analytics = Analytics()
        self.__cache = Cache()
        self.__watcher = None
        self.__pool = None

        # watcher is only available for Linux
        if LINUX:
            self.__watcher = Watcher()
            self.__pool = ManagerPool()

        # checking for EAST MODEL env var
        try:
            self.__textual = Textual()
        except EastModelEnvironmentMissing:
            Log.e(EastModelEnvironmentMissing.cause)
            return

        # communication links
        self.__progress_parent_pipe, self.__progress_child_pipe = None, None
        self.__logger_pipe = Queue()
        self.__video_pipe = None

        # communication for logs to ui
        Log.set_handler(self.__logger_pipe)

    def start_processing(self, app, input_file, intro=None, extro=None):
        """
        Process the input file call splitting function to split the input video file into
        audio and create 3 processes each for feature ranking, After completion of all the
        processes (waiting). Call the completed process method the start the timestamp
        extraction from the ranks

        Parameters
        ----------
        app : some controller object
            handles ui interactions
        input_file : str
            input video file (validating if its in supported format)
        intro : str
            name of the intro video file
        extro : str
            name of the extro video file

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

        # adding optional video file
        self.__ffmpeg.set_intro_video(intro)
        self.__ffmpeg.set_outro_video(extro)

        # saving the instance of the ui controller
        self.__App = app

        if self.__App is not None:

            # setting watcher to enabled
            if self.__watcher is not None:
                self.__watcher.enable(self, enable=True)

            # creating pipe for progress bar communication
            self.__progress_parent_pipe, self.__progress_child_pipe = Pipe()

            # starting listening on the communication link
            Thread(target=self.set_percent, args=()).start()
            Thread(target=self.set_log, args=()).start()

            # initialize the queue and thread
            if self.__video_display:
                self.__video_pipe = Queue()
                self.__visual.set_pipe(self.__video_pipe)
                Thread(target=self.set_video, args=()).start()

        # if from terminal
        else:
            self.__text_detect_display = True

        if not os.path.isfile(input_file):
            Log.e(f"Video file does not exists.")
            return

        if not check_type_video(input_file):
            return

        if self.__ffmpeg.split_video_audio(input_file):
            Log.d("The input video has been split successfully")
        # something went wrong [mostly video does not contain any audio]
        else:
            Log.e("Logging out")
            return

        self.__video_file = input_file
        self.__output_file = self.__ffmpeg.get_output_file_name_path()
        self.__audio_file = self.__ffmpeg.get_input_audio_file_name_path()
        self.__de_noised_audio_file = self.__ffmpeg.get_output_audio_file_name_path()

        # starting the sub processes
        self.__start_modules()

    def __start_modules(self):
        """
        Creating 3 processes using the Process class of the multi-processing module.
        FFmpeg separated files are referenced from the Controller public variables
        """

        if self.__watcher is not None:
            self.__watcher.start()  # starting the watcher

        self.__audio_process = Process(target=self.__auditory.start_processing,
                                       args=(self.__audio_file,
                                             self.__de_noised_audio_file,
                                             self.__snr_plot_display))

        self.__visual_process = Process(target=self.__visual.start_processing,
                                        args=(self.__progress_child_pipe,
                                              self.__video_file,
                                              self.__video_display))

        self.__textual_process = Process(target=self.__textual.start_processing,
                                         args=(self.__video_file,
                                               self.__text_detect_display))

        # starting the processes
        self.__audio_process.start()
        self.__visual_process.start()
        self.__textual_process.start()

        # adding the processes to the manager pool
        self.__pool.add(self.__audio_process.pid)
        self.__pool.add(self.__visual_process.pid)
        self.__pool.add(self.__textual_process.pid)

        # waiting for the processes to terminate
        self.__audio_process.join()
        self.__visual_process.join()
        self.__textual_process.join()

        # running the final pass
        self.__completed()

    def __completed(self):
        """
        Calls the merging function to merge the processed audio and the input
        video file. Once completed final video is outputted and the audio files
        generated are deleted as a part of the clean up process. Along with it
        the garbage collection module does some clean ups too.
        """

        if self.__watcher is not None:
            self.__watcher.stop()  # ending the watcher

        rankings = read_rankings()
        if self.__analytics_display:
            #  separate process for analytics
            Process(target=self.__analytics.analyze, args=(rankings,)).start()

        # cache file got missing
        try:
            timestamps = get_timestamps(data=rankings)
        except RankingOfFeatureMissing:
            Log.e(RankingOfFeatureMissing.cause)
            return

        # merging the final video
        if self.__ffmpeg.merge_video_audio(timestamps):
            Log.d("Merged the final output video ...............")
        else:
            return

        self.__ffmpeg.clean_up()
        self.__App.set_percent_complete(100.0)
        Log.set_handler(None)

    def clean(self):
        """ clean up """

        # terminating all processing tasks
        if self.__visual_process is not None:
            self.__visual_process.terminate()

        if self.__audio_process is not None:
            self.__audio_process.terminate()

        if self.__textual_process is not None:
            self.__textual_process.terminate()

        # closing all communication links
        if self.__progress_parent_pipe is not None:
            self.__progress_parent_pipe.close()

        if self.__progress_child_pipe is not None:
            self.__progress_child_pipe.close()

        Log.d("Terminating the processes")
        Log.d(f"Garbage collecting .. {gc.collect()}")

    def __del__(self):
        """ clean up """
        self.clean()

    def __close_comm(self):
        """ Close all the pipes """
        if self.__progress_parent_pipe is not None:
            self.__progress_parent_pipe.close()
        if self.__progress_child_pipe is not None:
            self.__progress_child_pipe.close()

    def set_save_logs(self, value=False):
        """ Save all the logs to a file """
        Log.toFile = value

    def set_video_display(self, value=False):
        """ Display the processing video output """
        self.__video_display = value

    def set_snr_plot(self, value=False):
        """ Display the snr plot for the audio """
        self.__snr_plot_display = value

    def set_ranking_plot(self, value=False):
        """ Display the analytics """
        self.__analytics_display = value

    def set_percent(self):
        """ Send the signal to the ui with the percentage of processing """
        while True:
            value = self.__progress_parent_pipe.recv()

            # checking whether the request is from UI
            if self.__App is not None and value is not None:
                self.__App.set_percent_complete(value)

                if value == 99.0:
                    self.__App.set_video_close()
                    self.__close_comm()
                    break

            else:
                sleep(0.1)

    def set_log(self):
        """ Send the signal to the ui with the log of the processing """
        while True:
            try:
                message = self.__logger_pipe.get()

                # checking whether the request is from UI
                if self.__App is not None and message is not None:
                    self.__App.set_message_log(message)
                else:
                    sleep(0.3)
            except EOFError as _:
                pass

    def set_video(self):
        """ Send the signal to the ui with the video frame to display """
        while True:
            try:
                frame = self.__video_pipe.get()

                # checking whether the request is from UI
                if self.__App is not None and frame is not None:
                    self.__App.set_video_frame(frame)
                else:
                    sleep(0.2)
            except EOFError as _:
                pass

    def set_cpu_complete(self, val):
        """ Send the signal to the ui with the percent usage of the cpu """
        # checking whether the request is from UI
        if self.__App is not None:
            self.__App.set_cpu_complete(val)

    def set_mem_complete(self, val):
        """ Send the signal to the ui with the percent usage of the ram/memory """
        # checking whether the request is from UI
        if self.__App is not None:
            self.__App.set_mem_complete(val)
