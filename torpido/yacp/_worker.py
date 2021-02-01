from ._utils import *


@override
def load(filename: str, cls, override=False, syntax=None):

    # returns the class reference, not the object
    Parser = get_parser_for_file(filename)

    if syntax is not None:
        parser = Parser(filename, syntax)
    else:
        parser = Parser(filename)

    # get the dictionary data
    dict_data = parser.deserialize()
    populated_object = populate(dict_data, cls)

    return populated_object


def dump(filename: str, cls, syntax=None):

    # return the class reference of the parser
    Parser = get_parser_for_file(filename)

    if syntax is not None:
        parser = Parser(filename, syntax)
    else:
        parser = Parser(filename)

    # write the dictionary data
    dict_data = allocate(cls)
    parser.serialize(dict_data)

    return True


def populate(data: dict, cls):
    # reading the members of the class and mapping
    # the values from the data, if match not found
    # it is skipped. 
    # TODO: add some message for no matches
    updated_cls = setmembers(data, cls)
    return updated_cls


def allocate(cls):
    # reading the members of the class and mapping
    # the values from the class to create a dictionary
    # to be dumped via the parser
    # TODO: parsing exceptions 
    data = getmembers(cls)
    return data
