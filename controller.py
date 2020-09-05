from lib.io import FFMPEG

ffmpeg = FFMPEG()
if ffmpeg.splitVideoAudio("/home/atul/Videos/sample.mp4"):
    print("FILES SEPPARATED>>>>>>>>>>>>>>>>>>>>>>")

print("Controller print........................")
print(ffmpeg.getInputFileNamePath())
print(ffmpeg.getOutputFileNamePath())
print(ffmpeg.getOutputAudioFileName())

if ffmpeg.mergeAudioVideo():
    print("FILES MERGED>>>>>>>>>>>>>>>>>>>>>>")
