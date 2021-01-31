"""
A simple cache storage helper to store minimal amount of data
in the dictionary, if data exists it will return the val or None
"""

from joblib import dump, load

from torpido.config.constants import *
from torpido.tools.logger import Log


class Cache:
    """
    Stores a dictionary as a file using joblib. Key-value pair of any object type can be saved.

    Attributes
    ----------
    __file_name : str
        file path and name for the cache file to store the data
    """

    def __init__(self):
        if not os.path.isdir(os.path.join(os.getcwd(), CACHE_DIR)):
            os.mkdir(os.path.join(os.getcwd(), CACHE_DIR))
        self.__file_name = os.path.join(os.getcwd(), CACHE_DIR, CACHE_NAME)

    def write_data(self, key, value):
        """
        Write the kay-value in the Cache file. If the file exists it would append the data to the dict object. Once data
        is written Log is printed using `Log` class

        Parameters
        ----------
        key : str
            Key value for the object to store
        value : object
            Value to store any object can be store

        """
        if os.path.isfile(self.__file_name):
            data = load(self.__file_name)
        else:
            data = dict()

        data[key] = value
        dump(data, self.__file_name)
        Log.d(f"[CACHE] : {key} is stored")

    def read_data(self, key):
        """
        Read value for the key in cache if cache does not exists or cache file itself is not present the Log is
        printed stating that Cache does not exists

        Parameters
        ----------
        key : str
            Key of the data to look for

        Returns
        -------
        result
            if exists cache else None
        """
        if os.path.isfile(self.__file_name):
            data = load(self.__file_name)
            return data[key] if key in data else None

        Log.e(f"[CACHE] : Cache does not exists yet")
        return None
