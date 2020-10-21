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


class RankingOfFeatureMissing(Exception):
    """
    When due to some issue ranking for some feature(s) was
    not created, then exception will be raised.
    """
    cause = "Rank for some feature in missing"


class EastModelEnvironmentMissing(Exception):
    """
    When the model path is read and the environment variable
    is missing or not yet set this error will be raised
    """
    cause = "EAST_MODEL environment variable is missing or incorrect"
