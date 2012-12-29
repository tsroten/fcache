# Copyright (c) 2012-2013 Thomas Roten

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnshished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""A simple file-based cache.

Classes:
    Cache: A cache that stores its data on the file system.

"""

import cPickle
import datetime
import hashlib
import os
import tempfile

import appdirs


class Cache(object):

    """A cache that stores its data on the file system.

    The cached data can be forced to expire after a certain amount of time or
    be kept indefinitely. The Cache class attempts to store cache files in the
    proper OS-designated (typically more of a convention) application cache
    directories.

    Example usage:
        import fcache
        # create a cache file named "temperatures" for the "weather-cli" app.
        current_weather = fcache.Cache("conditions", "weather-cli",
                                       "Joe Developer")
        # create some data that needs to be cached.
        boston_weather = {"temp": 64, "condition": "cloudy"}
        # cache the weather data in the "boston" key for 1 hour.
        current_weather.set("boston", boston_weather, 60 * 60)
        # get the data from the cache file.
        print current_weather.get("boston")["temp"]
        # -> 64

    Methods:
        get: read data key from the cache file
        set: store data key into the cache file
        remove: delete a key from the cache file
        delete: delete the cache file and all data in it.


    """

    def __init__(self, cachename, appname, appauthor=None):
        """Setup a Cache object.

        This method creates a cache file if there isn't one
        already created for [cachename].

        Args:
            cachename: a unique name for this cache file.
            appname: the name of this application -- used to determine the
                correct cache directory to store files in.
            appauthor: the name of this apps author or company -- used to
                determine the correct cache directory, in Windows,  to store
                files in.
        Raises:
            TypeError: 'appauthor' was not provided, but is needed
                because the host system is running Windows.

        """
        self.cachename = cachename
        try:
            self.cachedir = appdirs.user_cache_dir(appname, appauthor)
        except AppDirsError:
            raise TypeError("'user_cache_dir' expects 'appauthor' on Windows,"
                            "but received None")
        self.filename = os.path.join(self.cachedir,
                                     hashlib.md5(cachename).hexdigest())
        if os.access(self.filename, os.F_OK) is False:
            self._create()

    def get(self, name):
        """Get data from the cache.

        Args:
            name: the key name of the data.
        Returns:
            data: the asked-for data; or None if couldn't be retrieved.

        """
        data = self._read()
        if data is None or name not in data:
            return None
        if ((data[name]["expires"] is None) or
                ((datetime.datetime.now() -
                  data[name]["expires"]).total_seconds() < 0)):
            return data[name]["data"]
        else:
            return None

    def set(self, name, value, timeout=None):
        """Store data in the cache.

        Args:
            name: the name given to the data; to be used for retrieval.
            value: the data to be stored.
            timeout: how long in seconds the data should be considered
                valid -- defaults to forever.

        """
        data = self._read()
        if data is None:
            data = {}
        if timeout is None:
            expires = None
        else:
            expires = (datetime.datetime.now() +
                       datetime.timedelta(seconds=timeout))
        data[name] = {"expires": expires, "data": value}
        self._write(data)

    def remove(self, name):
        """Remove data from the cache.

        Args:
            name: the key name of the data to be removed.
        Returns:
            boolean: whether or not the data could be found and deleted.

        """
        data = self._read()
        try:
            del data[name]
        except KeyError:
            return False
        self._write(data)
        return True

    def delete(self):
        """Delete the cache file.

        NOTE: this removes all data from the cache.

        Returns:
            boolean: whether or not the file was found and successfully
                deleted.

        """
        try:
            os.remove(self.filename)
        except OSError:
            return False
        return True

    def _create(self):
        """Create a cache file."""
        if os.access(self.cachedir, os.F_OK) is False:
            os.makedirs(self.cachedir)
        f, tmp = tempfile.mkstemp(dir=self.cachedir)
        os.rename(tmp, self.filename)

    def _read(self):
        """Open a file and uses cPickle to retrieve its data"""
        with open(self.filename, "rb") as f:
            try:
                data = cPickle.load(f)
            except EOFError:
                return None
        return data

    def _write(self, data):
        """Use cPickle to save data to a file"""
        with open(self.filename, "wb") as f:
            cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL)
