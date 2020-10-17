"""
Utility functions to run subprocess with generated FFmpeg queries.
Function to build the commands live here.
"""

import subprocess

from lib.exceptions.custom import AudioStreamMissingException, FFmpegProcessException
from lib.util.logger import Log


def buildSplitCommand(inputFile, outputAudioFile):
    """
    Creates a list for each bit of the command line to run
    since it is a list the command line is secure and can
    run with file names that are not formatted correctly.
    or doesn't need any explicit formatting.

    Parameters
    ----------
    inputFile : str
        input video file name and path
    outputAudioFile : str
        output audio file name and path

    Returns
    ---------
    _CMD
        command line to pass to the subprocess

    Examples
    ----------
    The command created spits the video file into an audio file, The file paths
    are kept same. The command goes like this

    `ffmpeg -y -i input.mkv output.wav`

        '-y' : FFmpeg option for 'yes override'. Override the output file it exists
        '-i' : FFmpeg option for 'input file'. Input file can be multiple

    """
    return [
        'ffmpeg',
        '-y',
        '-i',
        str(inputFile),
        str(outputAudioFile)
    ]


def split(inputFile, outputAudioFile):
    """
    Splits the input video file into audio for Audio Processing.

    Helper function to run the generated command line with subprocess the stdout log is yielded to generate
    the progress bar. Look into `io` for details

    Parameters
    ----------
    inputFile : str
        name of the input video file
    outputAudioFile : str
        name of the output audio file

    Yields
    -------
    str
        yields std out logs in string
    """
    command = buildSplitCommand(inputFile, outputAudioFile)
    run = subprocess.Popen(args=command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           universal_newlines=True)
    for stdout in iter(run.stdout.readline, ""):
        yield stdout

    run.stdout.close()
    if run.wait():
        Log.e("The splitting process has caused an error.")
        raise AudioStreamMissingException


def buildMergeCommand(videoFile, audioFile, outputFile, timestamps):
    """
    Building a complex filter
    command line to clip portions based on the timestamps, the copies used
    to trim some portion depend on the length of the timestamps since that
    will define the number of the trims

    Parameters
    ----------
    videoFile : str
        original input video file
    audioFile : str
        processed audio file (de-noised)
    outputFile : str
        final output video file edited by Torpido
    timestamps : iterable
        start and end timestamps of the video clips to trim

    Returns
    -------
    str
        generated string from the complex filter built

    Examples
    --------
    The command line has following structure

    `
    ffmpeg -y -i input.mkv -i input.wav -filter_complex
    "[0:v]split=2[vc1][vc2];
    [vc1]trim=start=304:duration=10.567,setpts=PTS-STARTPTS[v1];
    [vc2]trim=start=100:duration=10.789,setpts=PTS-STARTPTS[v2];

    [1:a]asplit=2[ac1][ac2];
    [ac1]atrim=start=0:duration=10.123,asetpts=PTS-STARTPTS[a1];
    [ac2]atrim=start=304:duration=10,asetpts=PTS-STARTPTS[a2];

    [v1][a1][v2][a2]concat=n=2:v=1:a=1[video][audio]"
    -map "[video]" -map "[audio]" output_new.mkv
    `

        '-y' :              FFmpeg option for 'yes override'. Override the output file it exists
        '-i' :              FFmpeg option for 'input file'. Input file to the command can be multiple
        '-filter_complex' : create a complex filter
        'split' :           split option of filter to split the video stream into n ; here n=2
        'trim' :            trim option of filter to trim the video stream with
                            start= and duration=, also setpts:presentation points
        'asplit' :          audio stream split
        'atrim' :           audio stream trim
        'concat' :          concatenate input stream to output v=1:a=1 one video and one audio streams
        'map' :             map the labels of stream to the output file
        '[]' :              labels for each stream

    """
    filterString = 'ffmpeg' + \
                   ' -y' + \
                   ' -i ' + \
                   str(videoFile) + \
                   ' -i ' + \
                   str(audioFile) + \
                   ' -filter_complex ' + \
                   '"[0:v]split=' + str(len(timestamps))

    for i in range(len(timestamps)):
        filterString += '[vc%d]' % i
    filterString += '; '

    for i in range(len(timestamps)):
        startTime = timestamps[i][0]
        endTime = timestamps[i][1]
        filterString += '[vc%d]' % i
        filterString += 'trim=start=%f:duration=%f,setpts=PTS-STARTPTS[v%d]; ' \
                        % (startTime, (endTime - startTime), int(i))

    filterString += '[1:a]asplit=' + str(len(timestamps))
    for i in range(len(timestamps)):
        filterString += '[ac%d]' % i
    filterString += '; '

    for i in range(len(timestamps)):
        startTime = timestamps[i][0]
        endTime = timestamps[i][1]
        filterString += '[ac%d]' % i
        filterString += 'atrim=start=%f:duration=%f,asetpts=PTS-STARTPTS[a%d]; ' \
                        % (startTime, (endTime - startTime), int(i))

    for i in range(len(timestamps)):
        filterString += '[v%d][a%d]' % (i, i)
    filterString += 'concat=n=%d:v=1:a=1[video][audio]"' % (len(timestamps))

    filterString += ' -map' + \
                    ' "[video]"' + \
                    ' -map' + \
                    ' "[audio]" ' + \
                    str(outputFile)

    return filterString


def merge(videoFile, audioFile, outputFile, timestamps):
    """
    Generate the command for complex filter according to the timestamps and encode the output video. Merge the
    input video file and replace the audio stream with the de-noised audio stream

    Notes
    ------
    For using `string` as a command line it is very necessary to add shell=True in the Popen
    function argument or it won't work

    Use `stderr=subprocess.STDOUT` to stop printing the command output even though nothing
    is printing

    Parameters
    ----------
    videoFile : str
        input video file
    audioFile : str
        de-noised audio file
    outputFile : str
        final output video file
    timestamps : list
        list of clip time stamps with start and end times

    Yields
    -------
    str
        continuous std out logs
    """
    # print(f"[TIMESTAMPS] timestamps : {timestamps}")
    command = buildMergeCommand(videoFile, audioFile, outputFile, timestamps)
    # print(command)
    run = subprocess.Popen(args=command,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           universal_newlines=True)
    for stdout in iter(run.stdout.readline, ""):
        yield stdout

    run.stdout.close()
    if run.wait():
        Log.e(f"The merging process has caused an error.")
        raise FFmpegProcessException
