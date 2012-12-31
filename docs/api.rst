API
===

.. py:module:: fcache
.. class:: Cache(cachename, appname[, appauthor=None])

    Take *cachename* and *appname*, then create a cache file. If a matching cache file was found, a new one is not created.
    
    *appauthor* is used on Windows to determine the appropriate cache directory. If not provided, it defaults to *appname*. See :mod:`appdirs`'s documentation for more information.
    
    :param cachename: a unique name for the cache.
    :type cachename: :mod:`string`
    :param appname: the name of the application the cache is created for.
    :type appname: :mod:`string`
    :param appauthor: the name of the application's author -- if :data:`None`, defaults to *appname*.
    :type appauthor: :mod:`string` or :data:`None`

    .. attribute:: cachename
        
        The cache's name, as passed to the :class:`~fcache.Cache` constructor method. This attribute's value should not be changed unless you have good reason to do so.

    .. attribute:: cachedir

        The cache's parent directory, as determined by :meth:`appdirs.user_cache_dir`. This attribute's value should not be changed unless you have good reason to do so.

    .. attribute:: filename

        The cache's filename. It's formed by passing :attr:`~fcache.Cache.cachename` to :mod:`hashlib`'s :meth:`sha1` constructor. This attribute's value should not be changed unless you have **good reason** to do so. Editing it, then getting/setting data will most likely result in errors or lost data.
     
    .. method:: set(key, value[, timeout=None])

        Store data in the cache. The data, *value*, is stored under the name, *key*, in the cache. The data must be `picklable <http://docs.python.org/2.7/library/pickle.html#what-can-be-pickled-and-unpickled>`_. Optionally, the data can expire after *timeout* seconds have passed.

        :param key: the name given to the data.
        :type key: :mod:`string`
        :param value: the data to be stored.
        :param timeout: how long in seconds the data should be considered valid -- if :data:`None`, defaults to forever.
        :type timeout: :func:`int<int>`, :func:`long<long>`, :func:`float<float>`, or :data:`None`
        :raises pickle.PicklingError: an `unpicklable object <http://docs.python.org/2.7/library/pickle.html#what-can-be-pickled-and-unpickled>`_ was passed.
        :raises exceptions.IOError: the cache file does not exist or cannot be read.

    .. method:: get(key[, override=False])

        Get data from the cache. All data stored under the name, *key*, is returned. If the data is expired, ``None`` is returned. Expired data is returned if *override* is :data:`True`.

        :param key: the name of the data to fetch.
        :type key: :mod:`string`
        :param override: return expired data; defaults to :data:`False`.
        :type override: :func:`bool<bool>`
        :returns: the requested data or :data:`None` if the requested data has expired.
        :raises exceptions.KeyError: *key* was not found.
        :raises exceptions.IOError: the cache file does not exist or cannot be read.
        :raises pickle.UnpicklingError: there was a problem unpickling an object.

    .. method:: invalidate(key)

        Force data to expire. After forcing *key* to expire, calling :meth:`~fcache.Cache.get` on *key* will return :data:`None`.

        :param key: the name of the data to invalidate.
        :type key: :mod:`string`
        :raises exceptions.KeyError: *key* was not found.
        :raises exceptions.IOError: the cache file does not exist or cannot be read.

    .. method:: remove(key)

        Remove data from the cache. All data stored under *key* is deleted from the cache.

        :param key: the name of the data to remove.
        :type key: :mod:`string`
        :raises exceptions.KeyError: *key* was not found.
        :raises exceptions.IOError: the cache file does not exist or cannot be read.

    .. method:: flush()

        Clear all data from the cache. This removes all key/value pairs from the cache.

        :raises exceptions.IOError: the cache file does not exist.

    .. method:: delete()

        Delete the cache file.

        On Windows, if the file is in use by another application, an exception is raised. See :func:`os.remove` for more information.

        :raises exceptions.OSError: the cache file does not exist.
