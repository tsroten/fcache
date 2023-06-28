Welcome to fcache
=================

fcache is a dictionary-like, file-based cache module for Python. This is
fcache's documentation. It covers installation, a tutorial, and the API
reference.

Getting Started
---------------

Let's create a file cache:

.. code:: python

    >>> from fcache.cache import FileCache
    >>> mycache = FileCache('appname')

You can use the cache just like a :class:`dict`:

.. code:: python

    >>> mycache['foo'] = 'value'
    >>> mycache['foo']
    'value'
    >>> mycache['bar'] = 'blah'
    >>> list(mycache)
    ['foo', 'bar']
    >>> del mycache['bar']

By default, the cache object stores changes in a buffer that needs to be
explicitly synced with the cache's files:

.. code:: python

    >>> mycache.sync()
    >>> # closing a cache also syncs it:
    ... mycache.close()

If you want the cache to automatically write changes to disk everytime you
add/modify values, open the cache and append ``'s'`` to the optional *flag*
argument:

.. code:: python

    >>> mycache = FileCache('appname', flag='cs')

The ``'c'`` means that the object will open a cache if it exists, but will
create a new one if no cache is found. The ``'s'`` means that the cache is
opened in sync mode. All changes are immediately written to disk.

Using fcache with a :class:`~shelve.Shelf`
------------------------------------------

Python's :class:`~shelve.Shelf` class provides a persistent dictionary-like
object. Shelves normally use the :mod:`dbm` module as a backend. You can use easily use
fcache as a shelf's backend if needed. Because shelves already serialize data,
you'll need to tell fcache not to serialize the data:

.. code:: python

    >>> mycache = FileCache('appname', serialize=False)
    >>> myshelf = Shelf(mycache)

That's it! You can use the :class:`~shelve.Shelf` just like you normally
would.


Documentation Contents
----------------------

.. toctree::
    :maxdepth: 2

    installation
    api
    contributing
    authors
    history