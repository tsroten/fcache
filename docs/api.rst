API
===

.. automodule:: fcache.cache

.. autoclass:: FileCache

    .. data:: cache_dir

        The absolute path to the directory where the cache files are stored.
        The *appname* passed to :class:`FileCache` is used to determine a
        system-appropriate place to store the cache files.

    .. automethod:: close
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: sync

    In addition to the four methods listed above, :class:`FileCache` objects
    also support the following standard :class:`dict` operations and methods:

    .. describe:: list(f)

        Return a list of all the keys used in the :class:`FileCache` *f*.

    .. describe:: len(f)

        Return the number of items in the :class:`FileCache` *f*.

    .. describe:: f[key]

        Return the item of *f* with key *key*. Raises a :exc:`KeyError` if *key*
        is not in the cache.

    .. describe:: f[key] = value

        Set ``f[key]`` to *value*.

    .. describe:: del f[key]

        Remove ``f[key]`` from *f*.  Raises a :exc:`KeyError` if *key* is not in the
        cache.

    .. describe:: key in f

        Return ``True`` if *f* has a key *key*, else ``False``.

    .. describe:: key not in f

        Equivalent to ``not key in f``.

    .. describe:: iter(f)

        Return an iterator over the keys of the cache.  This is a shortcut
        for ``iter(f.keys())``.

    .. automethod:: clear()

    .. method:: get(key[, default])

        Return the value for *key* if *key* is in the cache, else *default*.
        If *default* is not given, it defaults to ``None``, so that this method
        never raises a :exc:`KeyError`.

    .. method:: items()

        Return a new view of the cache's items (``(key, value)`` pairs).
        See the :ref:`documentation of view objects <dict-views>`.

    .. method:: keys()

        Return a new view of the cache's keys.  See the :ref:`documentation
        of view objects <dict-views>`.

    .. method:: pop(key[, default])

        If *key* is in the cache, remove it and return its value, else return
        *default*.  If *default* is not given and *key* is not in the cache,
        a :exc:`KeyError` is raised.

    .. method:: popitem()

        Remove and return a ``(key, value)`` pair from the cache.

    .. method:: setdefault(key[, default])

        If *key* is in the cache, return its value.  If not, insert *key*
        with a value of *default* and return *default*.  *default* defaults to
        ``None``.

    .. method:: update([other])

        Update the cache with the key/value pairs from *other*, overwriting
        existing keys.  Return ``None``.

    .. method:: values()

        Return a new view of the cache's values.  See the
        :ref:`documentation of view objects <dict-views>`.