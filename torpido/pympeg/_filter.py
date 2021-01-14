"""
Creates complex and simple filters based on following functions
builds a chain of functions each containing a type of Node that
linked using the Label that identifies the stream and builds the
filter and is understandable by the ffmpeg command line.
"""

import os
from subprocess import Popen, PIPE

from ._builder import Stream
from ._exceptions import *
from ._node import (InputNode, FilterNode, Label,
                    OptionNode, OutputNode, GlobalNode, stream)
from ._util import get_str_from_filter, get_str_from_global
from torpido import ffpbar


__all__ = ["input", "filter", "output", "arg", "run", "graph", "option",
            "concat", "init", "scale", "crop", "setpts", "fade", "afade",
            "command"]
s = Stream()


def init():
    """ Re-initializes the stream object """
    global s
    s = Stream()


def _check_arg_type(args):
    """
    Only allow the following calling arguments to create a chain.
    The functions should be only callable by the following objects
    and the argument will be parsed as a node to create the chain.

    Parameters
    ----------
    args : list
        mostly caller of the function

    Returns
    -------
    bool
        passed/ fail criteria
    """
    flag = False

    for arg_ in args:
        if (
                isinstance(arg_, InputNode) or
                isinstance(arg_, OptionNode) or
                isinstance(arg_, FilterNode) or
                isinstance(arg_, GlobalNode) or
                isinstance(arg_, Label) or
                isinstance(arg_, list)
                ):
            flag = True
            break

    return flag


def _get_label_param(value):
    """
    Generate label based on the type of the object.
    This label gets added as the input to the node in
    the chain and creates a graph like structure.

    Parameters
    ----------
    value : object
        type of the object that is deduced below

    Returns
    -------
    Label
        label to link with the node from ip - > op
    """
    if value is None:
        return Label()

    if isinstance(value, Label):
        return value

    if isinstance(value, str):
        return Label(value)

    if isinstance(value, FilterNode):
        return value[0]

    if isinstance(value, InputNode):
        return Label(value.outputs)

    if isinstance(value, GlobalNode):
        return value[0]

    if isinstance(value, OptionNode):
        raise TypeMissing("Option nodes should be defined before the inputs.")

    else:
        raise TypeMissing("Filter requires an filter or input type argument")


def _get_nodes_from_graph(graph):
    """
    Separates the types of the nodes. Since, the links are
    directly attached to the node via the Label object and only
    the label matters at the end of the command, so distributing
    the nodes based on types helps create a command line argument.

    Parameters
    ----------
    graph : Sized, list-type
        output at the end of the run function. A list of all nodes

    Returns
    -------
    tuple
        distribution of all the nodes via their types
    """
    (
        input_nodes,
        option_nodes,
        filter_nodes,
        global_nodes,
        output_nodes
            ) = (
                    list(), list(),
                    list(), list(),
                    list()
                )

    for node in graph:
        if isinstance(node, InputNode):
            input_nodes.append(node)

        if isinstance(node, FilterNode):
            filter_nodes.append(node)

        if isinstance(node, OutputNode):
            output_nodes.append(node)

        if isinstance(node, GlobalNode):
            global_nodes.append(node)

        if isinstance(node, OptionNode):
            option_nodes.append(node)

    node_len = len(input_nodes) + len(option_nodes) + len(filter_nodes) + len(global_nodes) + len(output_nodes)
    assert node_len == len(graph)

    return input_nodes, option_nodes, filter_nodes, global_nodes, output_nodes


def _no_filter_command(input_nodes, output_nodes, option_nodes, cmd="ffmpeg"):
    """
    Cases when there is no filter. Mostly when conversion is required.

    Example
    -------
    ex: convert .mp4 to .wav
        ffmpeg -y -i example.mp4 example.wav
    """
    result = list()

    result.append(cmd)
    result.append(" -y")

    for inp in input_nodes:
        result.append(" -i %s " % inp.name)

    # adding option nodes in filter
    for opt in option_nodes:
        result.append(" %s %s " % (opt.tag, opt.name))

    for out in output_nodes:
        result.append("%s  %s " % (out.map, out.name))
    return ''.join(result)


def _get_command_from_graph(graph, cmd="ffmpeg"):
    """
    Generates the command line for the graph, this command is
    then ran using subprocess which will raise any exception or
    error on the ffmpeg side.

    Parameters
    ----------
    graph : list-type
        nodes from the end of the run function
    cmd : str
        ffmpeg default command, may changed based on alias

    Returns
    -------
    str
        string of the command to execute.

    Raises
    -------
    FFmpegException
        raised when the subprocess function fails.
    """
    result = list()
    input_nodes, option_nodes, filter_nodes, global_nodes, output_nodes = _get_nodes_from_graph(graph)

    # means that there is no filter
    if len(filter_nodes) == 0 and len(global_nodes) == 0:
        return _no_filter_command(input_nodes, output_nodes, option_nodes)

    # adding input nodes in fiter
    result.append(cmd)
    for inp in input_nodes:
        result.append(" -i %s " % inp.name)

    # adding option nodes in filter
    for opt in option_nodes:
        result.append(" %s %s" % (opt.tag, opt.name))

    # adding filter nodes in filter
    result.append(' -y -filter_complex "')
    for filter_ in filter_nodes:
        result.append(get_str_from_filter(filter_))

    # adding global nodes
    for global_ in global_nodes:
        result.append(get_str_from_global(global_))

    # getting rid of the semicolon at the end of the filter complex
    last_entry = result.pop()
    result.append(last_entry.replace(";", ""))
    result.append('"')

    # multiple output nodes
    for out in output_nodes:
        map_cmd = out.map
        for inp in out.inputs:
            result.append(' %s "[%s]"' % (map_cmd, inp.label))
        result.append(" %s " % out.name)

    return ''.join(result)


@stream()
def input(*args, name):
    """
    Creates the input node. Can create multiple input nodes.
    Requires the named argument to execute.
            ffmpeg -i input_example.mp4 -i input.mp3 ...

    Parameters
    ----------

    name : str
        name and path of the file

    Returns
    -------
    InputNode
        returns the input type of the node, which can recall this function

    Raises
    -------
    InputParamsMissing
        when the named argument (name) is missing.
    """
    if name is None:
        raise InputParamsMissing("File name required in input function")

    if not os.path.isfile(name):
        raise FileExistsError(f"Input file {name} does not exits.")

    # creating a file input filter
    node = InputNode(name, s.count)

    # adding to the stream
    s.add(node).count += 1

    return node


@stream()
def filter(*args, **kwargs):
    """
    Generates the filter based on the input caller, the input caller
    can be another filter node or any input node. Creates a Filter Node
    with input from the caller object.

    Parameters
    ----------
    args : list-type
            input args
    kwargs : dict-type
            name input args

    Returns
    -------
    FilterNode
            filter created for the input or another filter

    Raises
    -------
    TypeMissing
            caller is of some unknown type
    FilterParamsMissing
            filter was not able to create
    """
    if not _check_arg_type(args):
        raise TypeMissing("Filter requires an filter or input type argument")

    if len(kwargs) == 0:
        raise FilterParamsMissing

    # if explicit inputs are given skip caller
    if "inputs" in kwargs:
        inputs = kwargs["inputs"]
    # accept caller
    else:
        inputs = args[0]

    filter_node = FilterNode(**kwargs)

    if isinstance(inputs, list):
        for inp in inputs:
            filter_node.add_input(_get_label_param(inp))
    else:
        filter_node.add_input(_get_label_param(inputs))

    s.add(filter_node)
    return filter_node


@stream()
def output(*args, **kwargs):
    """
    Generates an OutputNode for the input filters or InputNodes
    The object gets parsed and the inputs are used for the map
    parameters in the ffmpeg command line

            ffmpeg .... -map "[label]" ... output.mp4

    Parameters
    ----------
    args : list-type
        input args
    kwargs : dict
        name input args

    Returns
    -------
    OutputNode
        output node for the filter or the input caller

    Raises
    -------
    TypeMissing
        caller is of some unknown type
    """
    if not _check_arg_type(args):
        raise TypeMissing("Output requires an filter or input type argument")

    if "name" not in kwargs:
        return None

    node = OutputNode(**kwargs)
    inputs = args[0]

    if isinstance(inputs, list):
        for inp in inputs:
            node.add_input(_get_label_param(inp))
    else:
        node.add_input(_get_label_param(inputs))

    s.add(node)
    return node


@stream()
def arg(caller=None, args=None, outputs=None, inputs=None):
    """
    Generates the GlobalNode for any filter types that cannot be
    created by the filter function. One of such filter is the concat.
    Other functions that do not follow the same syntax rules like filters.
    Then any function can be created and the command line argument can
    be directly stated using the names arguments (args), with inputs and outputs

    Also, concat function is available that is easy to use.

    Examples
    --------
        inputs : [0:v][0:a][3:v][3:a]

        ffmpeg.arg(inputs=["0:v", "0:a", "3:v", "3:a"], outputs=["video", "audio"],
                     args="concat=2:a=1:v=1")

         OP: [0:v][0:a][3:v][3:a] concat=2:a=1:v=1 [video][audio];
    Parameters
    ----------
    caller : any
        input for the Global Node
    args : str
        complete command with arguments can have any structure
    outputs : any
        outputs for the Global Node
    inputs : any
        inputs for the Global Node

    Returns
    -------
    GlobalNode
        global node that can have any structure with predefined function attributes.
    """
    node = GlobalNode(args=args)

    # if inputs is there don't check caller
    if inputs is not None:
        if isinstance(inputs, list):
            for inp in inputs:
                node.add_input(_get_label_param(inp))
        else:
            node.add_input(_get_label_param(inputs))

    # if inputs is absent
    else:
        if isinstance(caller, list):
            for inp in caller:
                node.add_input(_get_label_param(inp))
        else:
            node.add_input(_get_label_param(caller))

    # adding outputs, if none then 1 output is created by default
    if isinstance(outputs, list):
        for out in outputs:
            node.add_output(_get_label_param(out))
    elif isinstance(outputs, int):
        for _ in range(outputs):
            node.add_output(Label())
    else:
        node.add_output(_get_label_param(outputs))

    s.add(node)
    return node


@stream()
def option(*args, tag=None, name=None, output=None):
    """
    Adds a option node before the filters if any, this options can be 
    anything ffmpeg option defined as the tag and the name of the option
    Options like -f for file and other supported options.

        ffmpeg -f ffmetadata

        pympeg.option(tag="-f", name="ffmetadata", output="meta")

    Parameters
    ----------
    args : any
        arguments, caller object
    tag : str
        name of the option
    name : str
        the complete command
    output : any
        the output label for the node
    """
    outputs = list()

    if isinstance(output, list):
        for out in output:
            outputs.append(_get_label_param(out))
    else:
        outputs.append(_get_label_param(output))

    node = OptionNode(tag, name, output)
    s.add(node)

    return node


@stream()
def concat(*args, inputs:list, outputs:int):
    """
    Concat filter combines two or more streams into a single stream or a
    multiple streams video and audio. The input for the concat should be
    multiple of 2 (video1, audio1, video2, audio2) in this fashion if the
    outputs are 2, else it can have any number of imput.

    FFMPEG :: https://ffmpeg.org/ffmpeg-filters.html#toc-concat

    Ex 1: Cooncatenating two videos with audio

        ffmpeg -i ... "[0:v][0:a][1:v][2:v]concat=2:a=1:v=1[video][audio]"

        pympeg.concat(inputs=[inp.video, inp.audio, inp2.video, inp2.audio],
                        outputs=2)

    Ex 2: Concatenating two videos

        ffmeg -i ... "[inp][inp2]concat=2[video]"
        pympeg.concat(inputs=[inp, inp2], outputs=1)

    Parameters
    ----------
    args : any
        calling object
    inputs : list
        inputs for the concat filter can be labels or strings
    outputs : int
        no of outputs for the concat ideally one or two outputs are allowed.
    """
    if inputs is None:
        raise Exception("Concat requires inputs argument.")

    _inputs = list()
    if inputs is not None:
        if isinstance(inputs, list):
            for inp in inputs:
                _inputs.append(_get_label_param(inp))
        else:
            _inputs.append(_get_label_param(inputs))

    _outputs = list()
    if outputs > 1:
        for i in range(outputs):
            _outputs.append(Label())

        command = "concat=n=%d:v=%d:a=%d" % (len(_inputs) / 2, 1, 1)

    else:
        command = "concat=n=%d" % len(_inputs)

    # concat filter has different syntax so using Global Node
    node = GlobalNode(inputs=_inputs, args=command, outputs=_outputs)
    s.add(node)

    return node


@stream()
def crop(*args, w:str, h:str, x="0", y="0", keep_aspect=1):
    """
    The arguments for the crop function takes in str, since crop function can
    have complex equation and refernce to the input stream via ffmpeg convecction
    so not using int/float types directly.

    Also default keep_aspect of ffmpeg is 0, whereas I'm using 1 for making the 
    ratios of the input and the output same for more favourable use cases.

    FFMPEG  :: https://ffmpeg.org/ffmpeg-filters.html#toc-crop

    Parameters
    ----------
    args : any
        input for the filter
    w : str
        output stream width
    h : str
        output stream height
    x : str
        x positiion to place the video, default 0
    y : str
        y position to place the video, default 0
    keep_aspect : int
        if 1 aspect ratios is kept same between the ip and op, else not

    Returns
    -------
    FilterNode
        filter node is created
    """
    if not _check_arg_type(args):
        raise TypeMissing("Filter requires an filter or input type argument")

    _inputs = list()
    _inputs.append(_get_label_param(args[0]))

    node = FilterNode(
                inputs=_inputs,
                filter_name="crop",
                params={
                    "w": w,
                    "h": h,
                    "x": x,
                    "y": y,
                    "keep_aspect": keep_aspect
                }
            )

    s.add(node)

    return node


@stream()
def scale(*args, w:str, h:str):
    """
    Creates a scale filter with basic arguments with output width and height.
    Takes in a single input and one output.

    FFMPEG :: https://ffmpeg.org/ffmpeg-filters.html#toc-scale-1

    Parameters
    ----------
    args : any
        caller object
    w : str
        output width of the video
    h : str
        output height of the video

    Returns
    -------
    FilterNode
        filter node is created
    """
    if not _check_arg_type(args):
        raise TypeMissing("Filter requires an filter or input type argument")

    _inputs = list()
    _inputs.append(_get_label_param(args[0]))

    node = FilterNode(
                inputs=_inputs,
                filter_name="scale",
                params={
                    "w": w,
                    "h": h
                }
            )

    s.add(node)

    return node


@stream()
def run(caller, display_command=True):
    """
    Parses the entire chain of nodes, isolates the nodes based on types
    and generate a ffmpeg style command that will be run in the subprocess.
    Logs and errors are returned and final output can be created.

    Parameters
    ----------
    caller : OutputNode
        calling node, mostly an OutputNode

    Returns
    -------
    tuple
        log, error of just yield values

    Raises
    ------
    OutputNodeMissingInRun
        output node is required to run the ffmpeg command
    """
    if not isinstance(caller, OutputNode):
        raise OutputNodeMissingInRun

    graph = s.graph()
    command = _get_command_from_graph(graph)

    if display_command:
        print(command)

    progress = ffpbar.Progress()
    process = Popen(
            args=command,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            encoding='utf-8'
            )

    for out in process.stdout:
        progress.display(out)

    code = process.wait()

    if code:
        progress.clear()
        raise FFmpegException(
                'ffmpeg',
                ''.join(process.stderr.readlines()[-10: ]),
                'Error code :: %s' % code
            )


@stream()
def setpts(*args, expr="setpts=PTS-STARTPTS"):
    """
    Function to set the presentation timestamps of the input frames based on the
    expression according to the docs can have some expression that parses the
    input stream to generate. The default value is PTS-STARPTS, i.e. the timestamps
    starts from zero.

    FFMPEG ::  https://ffmpeg.org/ffmpeg-filters.html#toc-setpts_002c-asetpts

    Parameters
    ---------
    args : any
        caller object
    expr : str
        expression for the timestamps

    Returns
    -------
    GlobalNode
        global node for the setpts command
    """
    input_node = args[0]
    inputs = list()
    inputs.append(_get_label_param(input_node))

    node = GlobalNode(
            inputs=inputs,
            args=expr,
            outputs=Label()
            )

    s.add(node)
    return node


@stream()
def fade(*args, typ="in", st=0, d=5, color="black"):
    """
    Filter for applying fade in/out effects to the video stream, takes in type,
    start time, duration, and color parameters.

        ffmpeg -i .... "[0] afade=type=in:st=0:d=10:color=black[video]" ...

    Parameters
    ----------
    args : any
        caller object
    typ : str
        type of fade filter options :: (in, out)
    st : int
        start time of the fade effect, default is 0.
    d : int
        duration of fade, default is 5 sec
    color : str
        color of the fade, default black (ffmpeg default)

    Raises
    ------
    TypeMissing
        caller object is not of the accepted
    """
    if not _check_arg_type(args):
        TypeMissing("Fade filter required an input or filter type object.")

    input_node = args[0]
    inputs = list()
    inputs.append(_get_label_param(input_node))

    node = FilterNode(
            filter_name= fade.__name__,
            params={
                "type": typ,
                "st": st,
                "d": d,
                "color": color
                },
            inputs=inputs
            )

    s.add(node)
    return node


@stream()
def afade(*args, typ="in", st=0, d=5, curve="tri"):
    """
    Filter for applying fade in/out effects to the audio stream, takes in type,
    start time, duration, and curve parameters.

        ffmpeg -i .... "[0] afade=type=in:st=0:d=10:curve=tri[audio]" ...

    Parameters
    ----------
    args : any
        caller object
    typ : str
        type of fade filter options :: (in, out)
    st : int
        start time of the fade effect, default is 0.
    d : int
        duration of fade, default is 5 sec
    curve : str
        shape of the fade, default tri (triangular ffmpeg default)

    Raises
    ------
    TypeMissing
        caller object is not of the accepted
    """
    if not _check_arg_type(args):
        TypeMissing("Audio Fade filter required an input or filter type object.")

    input_node = args[0]
    inputs = list()
    inputs.append(_get_label_param(input_node))

    node = FilterNode(
            filter_name= afade.__name__,
            params={
                "type": typ,
                "st": st,
                "d": d,
                "curve": curve
                },
            inputs=inputs
            )

    s.add(node)
    return node


@stream()
def graph(*args):
    """ Returns the chain of the nodes, printable for representations """
    return s.graph()

@stream()
def command(*args):
    """ Returns the command for the chain """
    graph = s.graph()
    command = _get_command_from_graph(graph)
    return command

