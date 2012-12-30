fcache
======

About
-----

fcache is a simple, persistent, file-based cache module for Python. It uses `cPickle <http://docs.python.org/2/library/pickle.html#module-cPickle>`_ to store objects into a cache file, `appdirs <http://pypi.python.org/pypi/appdirs>`_ to ensure that cache files are located in platform-appropriate, application-specific directories, and supports data expiration times.

It's Simple
-----------

.. code:: python

    >>> import fcache
    >>> cache = fcache.Cache("population", "statistics-fetcher")
    >>> cache.set("chicago", 9729825)
    >>> print cache.get("chicago")
    9729825

It's Persistent
---------------

.. code:: python

    >>> exit()
    $ python
    >>> import fcache
    >>> cache = fcache.Cache("population", "statistics-fetcher")
    >>> print cache.get("chicago")
    9729825

It's File-Based
---------------

.. code:: python

    >>> print cache.filename
    /Users/tsr/Library/Caches/statistics-fetcher/248081ecb337c85ec8e4330e6099625a

Documentation
-------------

`fcache's documentation <http://tsroten.github.com/fcache/>`_ contains a usage introduction along with an API overview. For more information on how to get started with fcache, be sure to read the documentation.

Bug/Issues Tracker
------------------

fcache uses its `GitHub Issues page <https://github.com/tsroten/fcache/issues>`_ to track bugs, feature requests, and support questions.

License
-------

fcache is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
