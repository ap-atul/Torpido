import subprocess


def buildSplitCommand(inputFile, outputAudioFile):
    """
    create a list for each bit of the command line to run
    since it is a list the command line is secure and can
    run with file names that are not formatted correctly.
    or doesn't need any explicit formatting.
    :param inputFile: string, input video file
    :param outputAudioFile: string, name of output audio file
    :return: list, command line

    -y : yes to overwrite if name exists, cases when processing
        is done on same files again, even after cleanup

    -i : input file, stream of the input video

    can add codec options later on (may be)

    ex: ffmpeg -i video.mkv audio.wav
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
    split the input video file into audio. Using the same input file
    for processing, since copying the video stream also does the audio

    :param inputFile: string, input video file name path
    :param outputAudioFile: string, output audio path name
    :return: yields continuous output from command line, raises
    :exception: ffmpeg error
    """
    command = buildSplitCommand(inputFile, outputAudioFile)
    run = subprocess.Popen(args=command,
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    for stdout in iter(run.stdout.readline, ""):
        yield stdout

    run.stdout.close()
    if run.wait():
        raise Exception(f"[ERROR] The splitting process has caused an error : {run.stderr.readlines}")


# def buildMergeCommand(videoFile, audioFile, outputFile):
#     """
#     create a list of command line arguments and file names that
#     will be merged, the ffmpeg tool with named arguments
#     :param videoFile: string, input video stream
#     :param audioFile: string, input audio stream
#     :param outputFile: string, output file name
#     :return: list, command line
#
#     -y : yes to overwrite if name exists, cases when processing
#         is done on same files again, even after cleanup
#
#     -i : input file, stream of the input video
#
#     -c:v & -c:a : select the video and audio stream only, since we are
#         replacing the original's video' audio stream.
#
#     -map 0:v:0 : map the first file's video stream to first output file
#     -map 1:a:0 : map the second file's audio stream to first output file
#
#     -shortest : the length of output file would be same to the length of
#             smaller length of the input file
#
#     ex: ffmpeg -y -i video.mkv -i audio.wav -c:v copy -c:a aac  -map 0:v:0 -map 1:a:0 -shortest merged.mp4
#     """
#     return [
#         'ffmpeg',
#         '-y',
#         '-i',
#         str(videoFile),
#         '-i',
#         str(audioFile),
#         '-c:v',
#         'copy',
#         '-c:a',
#         'aac',
#         '-map',
#         '0:v:0',
#         '-map',
#         ' 1:a:0',
#         '-shortest',
#         str(outputFile)
#     ]


def buildMergeCommand_2(videoFile, audioFile, outputFile, timestamps):
    """
    Building a complex filter
    command line to clip portions based on the timestamps, the copies used
    to trim some portion depend on the length of the timestamps since that
    will define the number of the trims
    :param videoFile: str, original video
    :param audioFile: str, de noised audio
    :param outputFile: str, output video to generate
    :param timestamps: lol, start and end (in secs)
    :return: str , command build (list didn't work so string)

    Example command line: (clipping two portions)
    ffmpeg -y -i input.mkv -i input.wav -filter_complex
    "[0:v]split=2[vc1][vc2];
    [vc1]trim=start=304:duration=10.567,setpts=PTS-STARTPTS[v1];
    [vc2]trim=start=100:duration=10.789,setpts=PTS-STARTPTS[v2];
    [1:a]asplit=2[ac1][ac2];
    [ac1]atrim=start=0:duration=10.123,asetpts=PTS-STARTPTS[a1];
    [ac2]atrim=start=304:duration=10,asetpts=PTS-STARTPTS[a2];
    [v1][a1][v2][a2]concat=n=2:v=1:a=1[video][audio]"
    -map "[video]" -map "[audio]" output_new.mkv
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
        starttime = timestamps[i][0]
        endtime = timestamps[i][1]
        filterString += '[vc%d]' % i
        filterString += 'trim=start=%f:duration=%f,setpts=PTS-STARTPTS[v%d]; ' \
                        % (starttime, (endtime - starttime), int(i))

    filterString += '[1:a]asplit=' + str(len(timestamps))
    for i in range(len(timestamps)):
        filterString += '[ac%d]' % i
    filterString += '; '

    for i in range(len(timestamps)):
        starttime = timestamps[i][0]
        endtime = timestamps[i][1]
        filterString += '[ac%d]' % i
        filterString += 'atrim=start=%f:duration=%f,asetpts=PTS-STARTPTS[a%d]; ' \
                        % (starttime, (endtime - starttime), int(i))

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
    this function is much more complicated than current signature
    we need to make the implementation later on, for now this is it
    :param timestamps: ranks -> time stamps converts
    :param outputFile: string, output video file
    :param videoFile: string, video stream
    :param audioFile: string, audio  stream (de-noised)
    :return yields a value but looked for exceptions only
    :exception ffmpeg error
    """
    print(f"[TIMESTAMPS] time stamps : {timestamps}")
    command = buildMergeCommand_2(videoFile, audioFile, outputFile, timestamps)
    run = subprocess.Popen(args=command,
                           shell=True,
                           stdout=subprocess.PIPE,
                           universal_newlines=True,
                           )
    for stdout in iter(run.stdout.readline, ""):
        yield stdout

    run.stdout.close()
    if run.wait():
        raise Exception(f"[ERROR] The merging process has caused an error.")
