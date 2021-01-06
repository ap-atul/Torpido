"""
Utility function to check if the input file belongs to one of the supported
formats and can be processed readily if not we will raise errors
"""

import os

from torpido.config.constants import SUPPORTED_VIDEO_FILES
from torpido.tools.logger import Log


def check_type_video(input_file):
    """
    Checks if the input file is a video and the file exists.
    Prints error is the file is not a video and processing is not done until
    the input file is a video file of the supported formats defined in the `constants` file

    Parameters
    ----------
    input_file : str
        input video file

    Returns
    -------
    bool
        True is the input file is a video and it exists in the directory or the path
    """
    if os.path.isfile(input_file) is False:
        Log.e("Input video file does not exists")
        return False

    extension = os.path.splitext(input_file)[1]
    if extension in SUPPORTED_VIDEO_FILES:
        return True

    Log.i(f"Supported formats : {SUPPORTED_VIDEO_FILES}")
    return False
