""" Parsers for the serialisation and deserialisation"""
from ._resolver import Resolver


__all__ = ["JsonParser", "YamlParser", "CustomParser"]

class Parser:

    def __init__(self, file=None, data=None, syntax=None):
        self.__name__ = "parser"

        self._file = file
        self._data = data
        self._syntax = syntax

    def __str__(self):
        return "@%s" % self.__name__

    @property
    def file(self):
        return self._file

    @property
    def data(self):
        return self._data

    @property
    def syntax(self):
        return self._syntax

    def set_file(self, file: str):
        self._file = file


class JsonParser(Parser):

    def __init__(self, file: str):
        super().__init__()
        self.__name__ = "Jsonparser"

        self._file = file
        self._syntax = "json"
        self._data = None

    def deserialize(self):
        import json

        data = ""
        with open(self._file, "r") as f:
            self._data = json.load(f)
            f.close()

        return self._data

    def serialize(self, data):
        import json

        with open(self._file, "w") as f:
            json.dump(data, f)
            f.close()


class YamlParser(Parser):

    def __init__(self, file: str):
        super().__init__()
        self.__name__ = "Yamlparser"

        self._file = file
        self._syntax = "yaml"
        self._data = None

    def deserialize(self):
        import yaml

        data = ""

        with open(self._file, "r") as f:
            self._data = yaml.load(f, yaml.FullLoader)
            f.close()

        return self._data

    def serialize(self, data: dict):
        import yaml

        with open(self._file, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
            f.close()


class CustomParser(Parser):
    def __init__(self, file: str, syntax: str):
        super().__init__()
        self.__name__ = "Customparser"

        self._file = file
        self._syntax = syntax
        self._data = None

        self._resolver = Resolver()

    def deserialize(self):
        self._data = dict()
        sep = self._syntax.replace("%s", "")
        new_line = "\n"

        with open(self._file, "r") as f:
            lines = f.readlines()

            for line in lines:
                key, val = line.replace("\n", "").split(sep)
                self._data[key] = self._resolver.resolve(val)

            f.close()

        return self._data

    def serialize(self, data: dict):
        sep = self._syntax.replace("%s", "")

        with open(self._file, "w") as f:
            for key, val in data.items():
                f.write("%s%s%s\n" % (str(key), sep, str(val)))

        f.close()
