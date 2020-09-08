from lib.auditory import Auditory
from lib.io import FFMPEG
from lib.visual import Visual

ffmpeg = FFMPEG()
if ffmpeg.splitVideoAudio("examples/example1_small.mp4"):
    print("FILES SEPPARATED>>>>>>>>>>>>>>>>>>>>>>")

print("Controller print........................")
print(ffmpeg.getInputFileNamePath())
print(ffmpeg.getOutputFileNamePath())
print(ffmpeg.getOutputAudioFileNamePath())

auditory = Auditory()
auditory.startProcessing(ffmpeg.getOutputAudioFileNamePath(), ffmpeg.getOutputAudioFileNamePath())
visual = Visual()
visual.startProcessing(ffmpeg.getInputFileNamePath())
