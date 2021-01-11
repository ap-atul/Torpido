""" All the node types """

from ._exceptions import *
from ._util import gen_labels


class Label:
    """
    Label class to add input and output label to each type of the node.
    If label string is provided same would be used else a generator will
    create a label of length 3 (alphabetic)

    Attributes
    -----------
    _label : str
            label for the identification
    """

    def __init__(self, label=None):
        if label is None:
            self._label = gen_labels()
        else:
            self._label = label

    def __repr__(self):
        """ Pretty print """
        return "[%s]" % self._label

    def __eq__(self, other):
        """ Equality check """
        return self.label == other.label

    @property
    def label(self):
        """ Returns the label """
        return self._label

    def set_label(self, label):
        """ Sets the custom label """
        self._label = label
        return self


class InputNode:
    """
    The input node is the input to the ffmpeg command that contains the file
    name (along with the path) along with an output that is used to identify
    the index of the input managed and assigned by the Stream class.

            ffmpeg -i example.mp4 -i example.mp3 ...

            mp4 = pympeg.input(name="example.mp4")
            mp3 = pympeg.input(name="example.mp3")

    Attributes
    ----------
    _name : str
            name of the input file
    _output : str
            label, representing the index of the input

    Raises
    -------
    InputParamsMissing
            name or the output label is missing
    """

    def __init__(self, name, output):
        if name is None or output is None:
            raise InputParamsMissing

        self._name = name
        self._output = str(output)

    def __repr__(self):
        """ Pretty print """
        return "@input %s" % self._name + " :output [%s]" % self._output

    @property
    def name(self):
        """ returns name of the file """
        return self._name

    @property
    def audio(self):
        """ returns the audio stream """
        return self._output + ":a"

    @property
    def video(self):
        """ returns the video stream"""
        return self._output + ":v"

    @property
    def outputs(self):
        """ returns the output label """
        return "%s" % self._output

    def set_name(self, name):
        """ set the name of the file """
        self._name = name
        return self


class OutputNode:
    """
    Output node that stores the output file name, there can be multiple outputs,
    mostly one, with file name and the input labels, theses input labels can be the
    filter outputs that are needed to define the incoming streams from the filters

            ffmpeg ... filter[output1][output2]" -map "[output1]" -map "[output1]" out.mp4

    Attributes
    ----------
    _name : str
            name of the output file
    _inputs : list
            list of the inputs for the node
    """

    def __init__(self, name=None, inputs=None, map_cmd="-map"):
        self._name = name
        self._map = map_cmd
        self._inputs = list()

        if inputs is not None:
            self._inputs = inputs

    def __repr__(self):
        """ Pretty print """
        result = list()
        result.append("@output %s %s :input=" % (self._name, self._map))

        for inp in self._inputs:
            result.append("%s " % inp)

        return ''.join(result)

    @property
    def name(self):
        """ Returns the name of the file of the node """
        return self._name

    @property
    def map(self):
        """ Returns the map command of the node """
        return self._map

    @property
    def inputs(self):
        """ Returns the input labels of the node """
        return self._inputs

    def set_name(self, name):
        """ sets the name of the output file """
        self._name = name
        return self

    def set_map(self, map_cmd):
        """ sets the map command for the output node """
        self._map = map_cmd
        return self

    def add_input(self, label):
        """ add the input label for the node """
        self._inputs.append(label)
        return self


class FilterNode:
    """
    FilterNodes manages the filters that have a name, parameters, input streams and
    output streams. This filters can be called by InputNode or GlobalNode.

            ffmpeg ... "[inp]filter_name=p_key=p_val:p_key=p_val[out];"

    Attributes
    ----------
    _filter : str-type
            name of the filter
    _params : dict
            parameters for the filter
    _inputs : list-type
            inputs Label type
    _outputs : int
            count of outputs
    """

    def __init__(self, filter_name=None, params=None, inputs=None, outputs=1):
        self._filter = filter_name
        self._params = dict()
        self._inputs = list()
        self._outputs = list()

        for _ in range(outputs):
            self._outputs.append(Label())

        if inputs is not None:
            self._inputs = inputs

        if params is not None:
            self._params = params

    def __repr__(self):
        """ Pretty print """
        result = list()

        result.append("@filter %s " % self._filter)

        result.append("input=")
        for inp in self._inputs:
            result.append("%s " % str(inp))

        result.append(" :output=")
        for out in self._outputs:
            result.append("%s " % str(out))

        result.append(" :params=")
        for para, val in self._params.items():
            result.append("%s:%s " % (para, val))

        return ''.join(result)

    @property
    def name(self):
        """ Returns the name of the filter """
        return self._filter

    @property
    def inputs(self):
        """ Returns the input labels of the node """
        return self._inputs

    @property
    def outputs(self):
        """ Returns the output labels of the node """
        return self._outputs

    @property
    def params(self):
        """ Returns the dict of the parameters of the filter """
        return self._params

    def add_input(self, label):
        """ Adds input labels to the filter node """
        self._inputs.append(label)
        return self

    def add_output(self, label):
        """ Adds output labels to the filter node """
        self._outputs.append(label)
        return self

    def set_inputs(self, inputs):
        """ Sets the inputs for the node """
        self_inputs = inputs
        return self

    def set_outputs(self, outputs):
        """ Sets the outputs for the node """
        self._outputs = outputs
        return

    def __getitem__(self, item):
        """ Returns the output label with the index """
        return self._outputs[item]


class GlobalNode:
    """
    GlobalNode helps in creating some argument based ffmpeg construct that
    cannot be created using the FilterNode, this takes in the name of the function
    and its parameter as the string

    Attributes
    ----------
    _args : str
        the complete command
    _inputs : list
        input labels for the command
    _outputs : list
        output labels for the command
    """

    def __init__(self, inputs=None, args=None, outputs=None):
        self._args = args
        self._inputs = list()
        self._outputs = list()

        if inputs is not None:
            if isinstance(inputs, list):
                self._inputs = inputs
            else:
                self._inputs = [inputs]

        if outputs is not None:
            if isinstance(outputs, list):
                self._outputs = outputs
            else:
                self._outputs = [outputs]

    def __repr__(self):
        """ Pretty print """
        result = list()
        result.append("@global %s :input=" % self._args)

        for inp in self._inputs:
            result.append("%s " % str(inp))

        result.append(" :output=")
        for out in self._outputs:
            result.append("%s " % str(out))

        return ''.join(result)

    @property
    def name(self):
        """ Returns the entire command """
        return self._args

    @property
    def inputs(self):
        """ Returns the input labels """
        return self._inputs

    @property
    def outputs(self):
        """ Returns the output labels """
        return self._outputs

    def add_input(self, label):
        """ Add a label to input of the node """
        self._inputs.append(label)

    def add_output(self, label):
        """ Add a label to output of the node """
        self._outputs.append(label)

    def set_inputs(self, inputs):
        """ Sets the inputs for the node """
        self._inputs = inputs
        return self

    def set_outputs(self, outputs):
        """ Sets the outputs for the node """
        self._outputs = outputs
        return self

    def __getitem__(self, item):
        """ Returns the output label for the index """
        return self._outputs[item]


class OptionNode:
    def __init__(self, tag=None, name=None, output=None):
        if tag is None or name is None:
            raise OptionNodeParamMissing

        self._tag = tag
        self._name = name
        self._output = output

    def __repr__(self):
        """ Pretty print """
        return "@option %s" % self._name + " :output [%s]" % self._output

    @property
    def name(self):
        """ returns name of the file """
        return self._name

    @property
    def tag(self):
        """returns the tag of the node """
        return self._tag

    @property
    def audio(self):
        """ returns the audio stream """
        return self._output + ":a"

    @property
    def video(self):
        """ returns the video stream"""
        return self._output + ":v"

    @property
    def outputs(self):
        """ returns the output label """
        return "%s" % self._output

    def set_name(self, name):
        """ set the name of the file """
        self._name = name
        return self

    def set_tag(self, tag):
        """ set the tag for the node """
        self._tag = tag
        return self


def stream_operator(stream_classes=None, name=None):
    """
    Decorator that assigns all the functions to the class type. This makes the functions
    like input, filter, output, arg, graph, and run callable by any node type
    Label, InputNode, FilterNode, OutputNode, and GlobalNode
    """

    def decorator(func):
        func_name = name or func.__name__
        [setattr(stream_class, func_name, func) for stream_class in stream_classes]

        return func

    return decorator


def stream():
    """ Decorator helper """
    return stream_operator(stream_classes=[Label, InputNode, FilterNode, OutputNode, GlobalNode, OptionNode], name=None)
