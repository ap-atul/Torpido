"""
A simple cache storage helper to store minimal amount of data
in the dictionary, if data exists it will return the val or
None
"""

from joblib import dump, load

from torpido.config.constants import *
from torpido.config.logger import Log


class Cache:
    """
    Stores a dictionary asa file using joblib. Key-value pair of any object type can be saved.

    Attributes
    ----------
    __fileName : str
        file path and name for the cache file to store the data
    """

    def __init__(self):
        if os.path.isdir(os.path.join(os.getcwd(), CACHE_DIR)) is False:
            os.mkdir(os.path.join(os.getcwd(), CACHE_DIR))
        self.__fileName = os.path.join(os.getcwd(), CACHE_DIR, CACHE_NAME)

    def writeDataToCache(self, key, value):
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
        if os.path.isfile(self.__fileName):
            data = load(self.__fileName)
            data[key] = value
            dump(data, self.__fileName)
        else:
            data = dict()
            data[key] = value
            dump(data, self.__fileName)

        Log.d(f"[CACHE] : {key} is stored")

    def readDataFromCache(self, key):
        """
        Read value for the key in cache if cache does not exists or cache file itself is not present the Log is
        printed stating that Cache does not exists

        Parameters
        ----------
        key : str
            Key of the data to look for

        Returns
        -------
        object
            if exists cache else None
        """
        if os.path.isfile(self.__fileName):
            data = load(self.__fileName)
            if key in data:
                return data[key]
            else:
                Log.e(f"[CACHE] : Requested {key} does not exists")
                return None
        else:
            Log.e(f"[CACHE] : Cache does not exists yet")
            return None
