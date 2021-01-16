"""
Utility functions to run subprocess with generated FFmpeg queries.
Function to build the commands live here.
"""

import subprocess

from torpido import pympeg
from torpido.exceptions.custom import AudioStreamMissingException
from torpido.tools.logger import Log


def split(input_file, output_audio_file):
    command = _build_split_command(input_file, output_audio_file)
    command = ' '.join(command)
    Log.i(command)

    for log in _ffmpeg_runner(command):
        yield log


def merge(video_file, audio_file, output_file, timestamps, intro=None, extro=None):
    command = _build_merge_command_v2(video_file, audio_file, output_file, timestamps, intro, extro)
    Log.i(command)

    for log in _ffmpeg_runner(command):
        yield log


def _ffmpeg_runner(command):
    run = subprocess.Popen(args=command,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           universal_newlines=True)
    for stdout in iter(run.stdout.readline, ""):
        yield stdout

    run.stdout.close()
    if run.wait():
        Log.e("The splitting process has caused an error.")
        raise AudioStreamMissingException


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


def get_width_height(video_file):
    """ Getting the original videos resolution """
    output = pympeg.probe(video_file)
    width, height = None, None

    for stream in output['streams']:
        if 'width' in stream and 'height' in stream:
            width = stream['width']
            height = stream['height']
            break

    if isinstance(width, int) and isinstance(height, int):
        return width, height

    return 1920, 720


def _build_merge_command_v2(video_file, audio_file, output_file, timestamps, intro=None, outro=None):

    # getting output video resolution using ffprobe
    output_width, output_height = get_width_height(video_file)

    # creating the input nodes
    in_file = pympeg.input(name=video_file)
    in_audio = pympeg.input(name=audio_file)

    if intro is not None:
        intro = pympeg.input(name=intro)

    if outro is not None:
        outro = pympeg.input(name=outro)

    # for multiple trims
    trim_filters = list()

    # creating splits and its output labels
    args = "split=%s" % len(timestamps)
    outputs = list()
    for i in range(len(timestamps)):
        outputs.append("split_%s" % str(i))
    split = pympeg.arg(inputs=in_file, args=args, outputs=outputs)

    # making trims and scaling them to the output resolution
    for i, times in enumerate(timestamps):
        start, duration = times

        # video trim and scale filter
        trim_filters.append(
            split[i]
                .filter(filter_name="trim", params={"start": start, "duration": duration})
                .setpts()
                .scale(w=str(output_width), h=str(output_height))
                .arg(args="setdar=dar=16/9")
        )

        # audio trim filter
        trim_filters.append(
            in_audio.filter(filter_name="atrim", params={"start": start, "duration": duration})
        )

    # scaling the intro and outro if present
    if intro is not None:
        intro_C = (
            intro
                .scale(w=str(output_width), h=str(output_height))
                .arg(args="setdar=dar=16/9")
        )
        trim_filters.insert(0, intro_C)
        trim_filters.insert(1, intro.audio)

    if outro is not None:
        outro_C = (
            outro
                .scale(w=str(output_width), h=str(output_height))
                .arg(args="setdar=dar=16/9")
        )
        trim_filters.insert(len(trim_filters), outro_C)
        trim_filters.insert(len(trim_filters), outro.audio)

    # final concatenation of all the streams
    op = (
        pympeg.concat(inputs=trim_filters, outputs=2)
    )

    # returning the command
    return pympeg.output([op[0], op[1]], name=output_file).command()
