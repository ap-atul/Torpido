import os
from._parser import JsonParser, YamlParser, CustomParser

# this will set the attributes from the
# config file even is the class does not 
# have that member.
#
# Ex: 
# class Student:
#   ...
#   self.name = None
#
# ..config.yaml
#   name: ABC
#   age: 20
#
# Here the yaml file has another value with key age, 
# but the class does not contain such member, we can
# use override to assign it anyway. 
OVERRIDE = False


def override(fun):

    def decorator(*args, **kwargs):
        # if true, set the global to true
        if 'override' in kwargs:
            global OVERRIDE

            if kwargs['override']:
                OVERRIDE = True

        return fun(*args, **kwargs)

    return decorator


def get_parser_for_file(filename):
    basename = os.path.basename(filename)

    if basename.endswith('.json'):
        return JsonParser

    if basename.endswith('.yaml'):
        return YamlParser

    return CustomParser


def setmembers(data, cls):
    for key, val in data.items():

        if OVERRIDE:
            setattr(cls, key, val)
            continue

        if key in cls.__dict__:
            setattr(cls, key, val)

    return cls


def getmembers(cls):
    data = dict()

    for key, val in cls.__dict__.items():
        if str(key).startswith("__") and str(key).endswith("__"):
            continue

        data[key] = val

    return data
