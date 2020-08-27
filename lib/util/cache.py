import os

from joblib import dump, load

from lib.util.constants import *

"""
A simple cache storage helper to store minimal amount of data
in the dictionary, if data exists it will return the val or
None
"""


class Cache:
    def __init__(self):
        """
        create the folder path for the cache to store
        """
        if os.path.isdir(CACHE_DIR) is False:
            os.mkdir(CACHE_DIR)
        self.fileName = os.path.join(CACHE_DIR, CACHE_NAME)

    def writeDataToCache(self, key, value):
        """
        write to cache based on the key and value
        :param key: the key to store
        :param value: the mapped value
        :return: None
        """
        if os.path.isfile(self.fileName):
            data = load(self.fileName)
            data[key] = value
            dump(data, self.fileName)

        else:
            data = dict()
            data[key] = value
            dump(data, self.fileName)

        print(f"CACHE STORAGE : {key} -> {value} is stored")

    def readDataFromCache(self, key):
        """
        check if the data is in the cache,
        if not None is returned
        :param key: key to get from cache
        :return: value for the key
        """
        if os.path.isfile(self.fileName):
            data = load(self.fileName)
            if key in data:
                return data[key]
            else:
                print(f"CACHE STORAGE : Requested {key} does not exists")
                return None
        else:
            print(f"CACHE STORAGE : Cache does not exists yet")
            return None
