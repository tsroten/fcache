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

"""A simple file-based cache module for Python.

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
    directories. See the appdirs module's documentation for information on
    where the cache directory on each system is.

    Example usage:
        import fcache
        nyc_weather = {"temp": "64", "condition": "cloudy"}
        current_weather = fcache.Cache("weather", "weather-cli")
        current_weather.set("nyc", nyc_weather, 60 * 60)
        print current_weather.get("nyc")
        # {"temp": "64", "condition": "cloudy"}

        The above code first creates a new Cache object named "weather"
        for the "weather-cli" application. New York's weather is saved 
        to the "nyc" key and set to expire in 1 hour. Then, New York's
        weather is retrieved from the cache file.

    Types of data that can be cached:
        NOTE: fcache supports any types that the pickle module supports:
        * None, True, and False
        * integers, long integers, floating point numbers, complex numbers
        * normal and Unicode strings
        * tuples, lists, sets, and dictionaries containing only picklable
            objects
        * functions defined at the top level of a module
        * built-in functions defined at the top level of a module
        * classes that are defined at the top level of a module
        * instances of such classes whose __dict__ or __setstate__() is
            picklable

        See the pickle module's documentation for more details.

    Methods:
        get: read data from the cache.
        set: store data in the cache.
        remove: remove data from the cache.
        flush: clear all data in the cache.
        delete: delete the cache file.

    """

    def __init__(self, cachename, appname, appauthor=None):
        """Setup a Cache object.

        This method creates a cache file if there isn't one
        already created. If the [cachename] file already exists,
        then it uses that file.

        Args:
            cachename: a unique name for this cache file.
            appname: the name of this application -- used to determine the
                correct cache directory to store files in.
            appauthor: the name of this apps author or company -- used ,
                in Windows, to determine the correct cache directory.
                If empty or not provided, defaults to [appname].
        Raises:
            appdirs.AppDirsError: the appdirs module raises this error when
                the host system is Windows and the "appauthor" argument
                was not provided.

        """
        if appauthor is None or appauthor == "":
            appauthor = appname
        self.cachename = cachename
        self.cachedir = appdirs.user_cache_dir(appname, appauthor)
        self.filename = os.path.join(self.cachedir,
                                     hashlib.md5(cachename).hexdigest())
        if os.access(self.filename, os.F_OK) is False:
            self._create()
            self.flush()

    def set(self, name, value, timeout=None):
        """Store data in the cache.

        Any picklable data can be stored in the cache. See the above Cache
        class docstring for more information.

        Args:
            name: the name given to the data; to be used for retrieval.
            value: the data to be stored.
            timeout: how long in seconds the data should be considered
                valid -- defaults to forever.
        Raises:
            PicklingError: an unpicklable object was passed, see the pickle
                module's documentation for more details.
            IOError: if the cache file has been deleted and you attempt to
                save data to it.

        """
        data = self._read()
        if timeout is None:
            expires = None
        else:
            expires = (datetime.datetime.now() +
                       datetime.timedelta(seconds=timeout))
        data[name] = {"expires": expires, "data": value}
        self._write(data)

    def get(self, name):
        """Get data from the cache.

        Args:
            name: the key name of the data.
        Returns:
            data: the requested data.
             OR
            None: the data has already expired.
        Raises:
            KeyError: the key [name] was not found in the data.
            IOError: if the cache file has been deleted and you attempt to
                read data from it.
            Most of the exceptions normally raised by unpickling can be raised:
                * UnpicklingError
                * AttributeError
                * ImportError
                * IndexError
                See the pickle module's documentation for more details.

        """
        data = self._read()
        if ((data[name]["expires"] is None) or
                ((datetime.datetime.now() -
                  data[name]["expires"]).total_seconds() < 0)):
            return data[name]["data"]
        else:
            return None

    def remove(self, name):
        """Remove data from the cache.

        This removes all data with key [name]. It does not delete any
        other data keys or delete the cache file itself.

        Args:
            name: the key name of the data to be removed.
        Raises:
            KeyError: the key [name] was not found in the data.
            IOError: if the cache file has been deleted and you attempt to
                remove data from it.

        """
        data = self._read()
        del data[name]
        self._write(data)

    def flush(self):
        """Clear all data in the cache.

        If there is data in the cache file, this will remove it, but will not
        delete the cache file itself.
        
        NOTE: If the cache file is already deleted, this will create a cache
        file with no data.

        """
        
        self._write({})

    def delete(self):
        """Delete the cache file.

        NOTE: this removes all data from the cache as well as the cache file
        itself.

        Raises:
            OSError: if the cache file has already been deleted and you attempt
                to delete it again.
            On Windows, an exception is raised if the file being removed
                is in use. See the os.remove method's documentation for more
                information. fcache closes files when it is done reading or
                writing, so this should not be a problem.

        """
        os.remove(self.filename)

    def _create(self):
        """Create a cache file."""
        if os.access(self.cachedir, os.F_OK) is False:
            os.makedirs(self.cachedir)
        f, tmp = tempfile.mkstemp(dir=self.cachedir)
        os.rename(tmp, self.filename)

    def _read(self):
        """Open a file and use cPickle to retrieve its data"""
        with open(self.filename, "rb") as f:
            return cPickle.load(f)

    def _write(self, data):
        """Open a file and use cPickle to save data to it"""
        with open(self.filename, "wb") as f:
            cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL)
