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

import datetime
import hashlib
import os
import pickle
import sys
import tempfile

import appdirs


class Cache(object):

    """A cache that stores its data on the file system.

    The cached data can be forced to expire after a certain amount of time or
    be kept indefinitely. The Cache class attempts to store cache files in the
    proper OS-designated (typically more of a convention) application cache
    directories.

    """

    def __init__(self, cachename, appname, appauthor=None):
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
        data = self._read()
        if data is None:
            return None
        if ((data[name]["expires"] is None) or
                ((datetime.datetime.now() -
                data[name]["expires"]).total_seconds() < 0)):
            return data[name]["data"]
        else:
            return None

    def set(self, name, value, timeout=None):
        data = self._read()
        if data is None:
            data = {}
        if timeout is None:
            expires = None
        else:
            expires = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        data[name] = {"expires": expires, "data": value}
        self._write(data)


    def remove(self, name):
        pass

    def delete(self):
        pass

    def _create(self):
        if os.access(self.cachedir, os.F_OK) is False:
            os.makedirs(self.cachedir)
        f, tmp = tempfile.mkstemp(dir=self.cachedir)
        os.rename(tmp, self.filename)

    def _read(self):
        with open(self.filename, "rb") as f:
            try:
                data = pickle.load(f)
            except EOFError:
                return None
        return data

    def _write(self, data):
        with open(self.filename, "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
