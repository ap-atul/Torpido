"""
All custom exceptions
"""


class AudioStreamMissingException(Exception):
    """
    When there is no audio in some input video files
    Exception will be raised along with the below message
    """
    cause = "There is not audio in the video file"


class FFmpegProcessException(Exception):
    """
    When the subprocess did not able to do the rendering or
    some other FFmpeg error, this exception would be raised
    """
    cause = "FFmpeg has some problem processing"
