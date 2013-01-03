fcache
======

About
-----

fcache is a simple, persistent, file-based cache module for Python. It uses `cPickle <http://docs.python.org/2/library/pickle.html#module-cPickle>`_ to store objects into a cache file and `appdirs <http://pypi.python.org/pypi/appdirs>`_ to ensure that cache files are stored in platform-appropriate, application-specific directories. It supports optional, time-based data expiration.

It's Simple
-----------

::

    >>> import fcache
    >>> cache = fcache.Cache("population", "statistics-fetcher")
    >>> cache.set("chicago", 9729825)
    >>> print cache.get("chicago")
    9729825

Using fcache is as simple as creating a ``Cache`` object, setting data, and getting data back.

It's Persistent
---------------

::

    >>> exit()
    $ python
    >>> import fcache
    >>> cache = fcache.Cache("population", "statistics-fetcher")
    >>> print cache.get("chicago")
    9729825

Cached data doesn't disappear when you stop using a ``Cache`` object. When you create a new object with the same arguments, your data is still there, just like you left it.

It's File-Based
---------------

::

    >>> print cache.filename
    /Users/tsr/Library/Caches/statistics-fetcher/248081ecb337c85ec8e4330e6099625a

Cached data is stored in a file, plain and simple. You can see it on the file system. You can delete it, copy it, or write your own library to open it.

It's Time-Aware
---------------

::

    >>> import time
    >>> cache.set("chicago", 9729825, 30)
    >>> print cache.get("chicago")
    9729825
    >>> time.sleep(30)
    >>> print cache.get("chicago")
    None

Just like an orange, some data goes bad after awhile. fcache can keep track of when data should expire.

Documentation
-------------

`fcache's documentation <https://fcache.readthedocs.org/>`_ contains an introduction along with an API overview. For more information on how to get started with fcache, be sure to read the documentation.

Bug/Issues Tracker
------------------

fcache uses its `GitHub Issues page <https://github.com/tsroten/fcache/issues>`_ to track bugs, feature requests, and support questions.

License
-------

fcache is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
