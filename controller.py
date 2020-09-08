import threading

from lib.auditory import Auditory
from lib.io import FFMPEG
from lib.textual import Textual
from lib.visual import Visual

ffmpeg = FFMPEG()
if ffmpeg.splitVideoAudio("examples/example1_small.mp4"):
    pass

print("Controller print........................")
print(ffmpeg.getInputFileNamePath())
print(ffmpeg.getOutputFileNamePath())
print(ffmpeg.getOutputAudioFileNamePath())

auditory = Auditory()
textual = Textual()
visual = Visual()

# audioThread = threading.Thread(target=auditory.startProcessing,
#                                args=(ffmpeg.getOutputAudioFileNamePath(), ffmpeg.getOutputAudioFileNamePath()))
visualThread = threading.Thread(target=textual.startProcessing,
                                args=(ffmpeg.getInputFileNamePath(), True))
# textualThread = threading.Thread(target=textual.startProcessing,
#                                  args=(ffmpeg.getInputFileNamePath(), False))

# audioThread.start()
visualThread.start()
# textualThread.start()


def done():
    ffmpeg.mergeAudioVideo()
