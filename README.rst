fcache
======

fcache is a dictionary-like, file-based cache module for Python. It's simple
to use, has an optional write buffer, and is
`Shelf <http://docs.python.org/3.3/library/shelve.html#shelve.Shelf>`_-compatible.

.. code:: python

    >>> from fcache.cache import FileCache
    >>> mycache = FileCache('cache_dir')
    >>> mycache['foo'] = [1, 2, 3, 4, 5]
    >>> mycache['foo']
    [1, 2, 3, 4, 5]
    >>> mycache['bar'] = 'value'
    >>> list(mycache)
    ['foo', 'bar']
    >>> del mycache['foo']
    >>> mycache['foo']
        ...
        KeyError: 'foo'

Install
-------

fcache supports Python 2.6, 2.7, and 3. To install fcache, use pip:

.. code:: bash

    $ pip install fcache

Documentation
-------------

`fcache's documentation <https://fcache.readthedocs.org/>`_ contains an introduction along with an API overview. For more information on how to get started with fcache, be sure to read the documentation.

Bug/Issues Tracker
------------------

fcache uses its `GitHub Issues page <https://github.com/tsroten/fcache/issues>`_ to track bugs, feature requests, and support questions.

License
-------

fcache is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
