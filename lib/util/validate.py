import os

from lib.util.constants import SUPPORTED_VIDEO_FILES
from lib.util.logger import Log

"""
utility file to check if the input file belongs to one of the supported
formats and can be processed readily if not we will raise errors
"""


def checkIfVideo(inputFile):
    if os.path.isfile(inputFile) is False:
        Log.e("Input video file does not exists")
        return False

    extension = os.path.splitext(inputFile)[1]
    if extension in SUPPORTED_VIDEO_FILES:
        return True

    Log.i(f"Supported formats : {SUPPORTED_VIDEO_FILES}")
    return False

