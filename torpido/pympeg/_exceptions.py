class FilterParamsMissing(Exception):
    """
    When some parameters are missing while initializing the Filter Node,
    this exception will be raised asking for the completion of the missing
    parameters
    """

    def __str__(self):
        return "Filter node has missing arguments. \n Use like :: " \
                """filter(filter_name="trim", params={"start": 10, "duration": 20})"""


class InputParamsMissing(Exception):
    """
    When name of the file is missing while initialization of the IONode,
    this exception will be raised asking for the missing name of the file.
    The file should be complete address not only the name of the file
    """

    def __str__(self):
        return "File name is missing for the input function. \n Use like :: " \
                """ pympeg.input(name="example.mp4") """


class  OptionNodeParamMissing(Exception):
    """
    When name of the file and tag is missing in the Option node initialization
    this exception would be raised. And corresponding node won't be created.
    """

    def __str__(self):
        return "Option tag has missing tag name or arguments. \n Use"\
                """pympeg.option(tag="-f", name="ffmetadata", "meta")"""


class TypeMissing(Exception):
    """
    When the type of the filter is missing from the important functions, this
    exception will be raised along with the message
    """
    pass


class ProbeException(Exception):
    """
    When the probe function runs into some error this exception would be raised,
    along with the command line output what so ever.
    """
    pass


class OutputNodeMissingInRun(Exception):
    """
    When the run function is called but the caller isn't a output node,
    then this exception would be raised.
    """

    def __str__(self):
        return "Output function is needed to called before the run function."


class FFmpegException(Exception):
    """
    When an error is thrown by the ffmpeg subprocess from the run function
    this exception would be raised that will print all the stdout of the
    ffmpeg output.
    """
    def __init__(self, cmd, stdout, stderr):
        self._stdout = stdout
        self._stderr = stderr

    def __str__(self):
        return '%s %s' % (self._stdout, self._stderr)

