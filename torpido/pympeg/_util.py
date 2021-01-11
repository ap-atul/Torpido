""" Utilities """

import string
from random import sample


def gen_labels(n=1):
    """ Randomly generate label of size 3 with alphabets """
    length = 3
    if n == 1:
        return ''.join(sample(string.ascii_letters, length))

    return [''.join(sample(string.ascii_letters, length)) for _ in range(n)]


def get_str_from_params(params: dict):
    """ Returns string from the parameters """
    result = list()
    keys = list(params.keys())
    length = len(keys)

    result.append("%s=%s" % (keys[0], params[keys[0]]))
    for i in range(1, length):
        result.append(":%s=%s" % (keys[i], params[keys[i]]))

    return ''.join(result)


def get_str_from_filter(filter):
    """ Returns the string from the filter """
    result = list()

    for inp in filter.inputs:
        result.append("[%s]" % inp.label)

    result.append(" %s=%s " % (filter.name, get_str_from_params(filter.params)))

    for out in filter.outputs:
        result.append("[%s]" % out.label)

    result.append(";")

    return ''.join(result)


def get_str_from_global(node):
    """ Returns the string from the global node """
    result = list()

    for inp in node.inputs:
        result.append("[%s]" % inp.label)

    result.append("%s" % node.name)

    for out in node.outputs:
        result.append("[%s]" % out.label)

    result.append(";")

    return ''.join(result)
