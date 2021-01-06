"""
Utility functions to run subprocess with generated FFmpeg queries.
Function to build the commands live here.
"""

import subprocess

from torpido.exceptions.custom import AudioStreamMissingException, FFmpegProcessException
from torpido.tools.logger import Log


def _build_split_command(input_file, output_audio_file):
    """
    Creates a list for each bit of the command line to run
    since it is a list the command line is secure and can
    run with file names that are not formatted correctly.
    or doesn't need any explicit formatting.

    Parameters
    ----------
    input_file : str
        input video file name and path
    output_audio_file : str
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
        str(input_file),
        str(output_audio_file)
    ]


def split(input_file, output_audio_file):
    """
    Splits the input video file into audio for Audio Processing.

    Helper function to run the generated command line with subprocess the stdout log is yielded to generate
    the progress bar. Look into `io` for details

    Parameters
    ----------
    input_file : str
        name of the input video file
    output_audio_file : str
        name of the output audio file

    Yields
    -------
    str
        yields std out logs in string
    """
    command = _build_split_command(input_file, output_audio_file)
    Log.i(command)

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


def _build_merge_command(video_file, audio_file, output_file, timestamps, intro=None, extro=None):
    """
    Building a complex filter
    command line to clip portions based on the timestamps, the copies used
    to trim some portion depend on the length of the timestamps since that
    will define the number of the trims

    Parameters
    ----------
    extro : str
        exit video
    intro : str
        intro video
    video_file : str
        original input video file
    audio_file : str
        processed audio file (de-noised)
    output_file : str
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
    timestamp_length = len(timestamps)

    command = ['ffmpeg',
               ' -y',
               ' -i ',
               str(video_file),
               ' -i ',
               str(audio_file)]

    if intro is not None:
        command.append(' -i %s' % str(intro))

    if extro is not None:
        command.append(' -i %s' % str(extro))

    command.append(' -filter_complex "[0:v]split=' + str(timestamp_length))

    # creating splits
    for i in range(timestamp_length):
        command.append('[vc%d]' % i)
        command.append('; ')

    # making trims
    for i in range(timestamp_length):
        startTime, endTime = timestamps[i]
        command.append(
            '[vc%d]trim=start=%f:duration=%f,setpts=PTS-STARTPTS,scale=1920:-1,crop=1920:1080:0:0[v%d]; '
            % (i, startTime, (endTime - startTime), int(i))
        )

    # creating audio splits
    command.append('[1:a]asplit=' + str(timestamp_length))
    for i in range(timestamp_length):
        command.append('[ac%d]' % i)
    command.append('; ')

    # making audio trims
    for i in range(timestamp_length):
        startTime, endTime = timestamps[i]
        command.append(
            '[ac%d]atrim=start=%f:duration=%f,asetpts=PTS-STARTPTS[a%d]; '
            % (i, startTime, (endTime - startTime), int(i))
        )

    concat = timestamp_length
    if intro is not None and extro is not None:
        concat += 1
        command.append('[2:v]scale=1920:-1,crop=1920:1080:0:0[intro];')
        command.append('[3:v]scale=1920:-1,crop=1920:1080:0:0[extro];')
        command.append('[intro][2:a]')

    for i in range(timestamp_length):
        command.append('[v%d][a%d]' % (i, i))

    if extro is not None:
        concat += 1
        command.append('[extro][3:a]')

    command.append('concat=n=%d:v=1:a=1[video][audio]"' % concat)

    command.extend([' -map',
                    ' "[video]"',
                    ' -map',
                    ' "[audio]" ',
                    str(output_file)])

    return "".join(command)


def merge(video_file, audio_file, output_file, timestamps, intro=None, extro=None):
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
    video_file : str
        input video file
    audio_file : str
        de-noised audio file
    output_file : str
        final output video file
    timestamps : list
        list of clip time stamps with start and end times
    intro : str
        intro video file
    extro : str
        extro video file

    Yields
    -------
    str
        continuous std out logs
    """
    command = _build_merge_command(video_file, audio_file, output_file, timestamps, intro, extro)
    Log.i(command)

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
