import re


class Resolver:
    resolvers = {
            "bool_y": re.compile(r'''^(?:yes|Yes|YES|true|True|TRUE|on|On|ON)$''', re.X),
            "bool_n": re.compile(r'''^(?:no|No|NO|false|False|FALSE|off|Off|OFF)$''', re.X),
            "int": re.compile(r'''^(?:[-+]?0b[0-1_]+|[-+]?0[0-7_]+|[-+]?(?:0|[1-9][0-9_]*)|[-+]?0x[0-9a-fA-F_]+|[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$''', re.X),
            "float": re.compile(r'''^(?:[-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?|\.[0-9_]+(?:[eE][-+][0-9]+)?|[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\.[0-9_]*|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$''', re.X),
            "none": re.compile(r'''^(?: ~|null|Null|NULL| )$''', re.X)
    }

    type_mappings = {
            "bool_y": True,
            "bool_n": False,
            "int": int,
            "float": float,
            "none": None
    }

    def __init__(self):
        self.type_rets = ["bool_y", "bool_n", "none"]

    def resolve(self, data):
        for key, reg_exp in self.resolvers.items():
            if reg_exp.match(data):
                if key in self.type_rets:
                    return self.type_mappings[key]

                _type = self.type_mappings[key]
                return _type(data)

        else:
            return str(data)

