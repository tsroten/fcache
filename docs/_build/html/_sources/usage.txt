Usage
=====

Let's learn how to use :mod:`fcache`.

Create a Cache
--------------

:mod:`fcache` consists of a single class, :class:`~fcache.Cache`.

.. code-block:: python

    >>> import fcache
    >>> cache = fcache.Cache("hello", "hello_goodbye")

By creating an instance of :class:`~fcache.Cache`, you've created a cache file on the file system that is identified as "hello" and associated with the "hello_goodbye" application.

Store Data in the Cache
-----------------------

.. code-block:: python

    >>> cache.set("english", "Hello!")
    >>> cache.set("spanish", u"¡Hola!")
    >>> cache.set("chinese", u"你好！")

By calling the method :meth:`~fcache.Cache.set`, you associate a *value* with a *key*, just like with a Python dictionary. In your cache file, there is now three key/value pairs.

Get Data from the Cache
-----------------------

.. code-block:: python

    >>> print cache.get("english")
    Hello!
    >>> print cache.get("spanish")
    ¡Hola!
    >>> print cache.get("chinese")
    你好！

By calling the method :meth:`~fcache.Cache.get`, you can retrieve the *value* of a *key*.

Store Other Types of Data
-------------------------

.. code-block:: python

    >>> english_greetings = {"ordinary": "Hello!", "friendly": "Hey there!"}
    >>> cache.set("english", english_greetings)
    >>> print cache.get("english")
    {'ordinary': 'Hello!', 'friendly': 'Hey there!'}

The data stored doesn't have to be a string. It can be any type that the :mod:`pickle`  module `supports <http://docs.python.org/2.7/library/pickle.html#what-can-be-pickled-and-unpickled>`_. In this case, we used a dictionary to store multiple English greetings.

Set Data to Expire After a Certain Time
---------------------------------------

.. code-block:: python

    >>> cache.set("norwegian", "Hallo!", 30)
    >>> print cache.get("norwegian")
    Hallo!
    >>> import time
    >>> time.sleep(30)
    >>> print cache.get("norwegian")
    None

Data can be set to expire after a certain amount of seconds. By setting data to expire in *30* seconds, you can fetch the data anytime in the next 30 seconds; after that, the data will return as ``None``. In this example, we used the :func:`time.sleep` function to wait 30 seconds so that the data would expire.

Invalidate Data
---------------

.. code-block:: python

    >>> print cache.get("english")
    {'ordinary': 'Hello!', 'friendly': 'Hey there!'}
    >>> cache.invalidate("english")
    >>> print cache.get("english")
    None

Data can be forced to expire, even if it doesn't have an expiration time. Once data is invalidated, calling :meth:`~fcache.Cache.get` on its *key* will return :data:`None`.

Remove Data From the Cache
--------------------------

.. code-block:: python

    >>> cache.remove("chinese")
    >>> cache.get("chinese")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/tsr/.virtualenvs/fcache/lib/python2.7/site-packages/fcache-0.1-py2.7.egg/fcache.py", line 163, in get
        if ((data[name]["expires"] is None) or
    KeyError: 'chinese'

Data can be easily removed from a cache by calling the :meth:`~fcache.Cache.remove` method. If you try to retrieve a key that doesn't exist, :exc:`exceptions.KeyError` is raised.

Cached Data is Persistent
-------------------------

.. code-block:: python

    >>> exit()
    $ python
    >>> import fcache
    >>> cache = fcache.Cache("hello", "hello_goodbye")
    >>> print cache.get("spanish")
    ¡Hola!

:mod:`fcache` provides persistent cache files. In other words, your cached data is saved even after you stop using it.

Clear Cached Data
-----------------

.. code-block:: python

    >>> cache.flush()
    >>> print cache.get("spanish")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/tsr/.virtualenvs/fcache/lib/python2.7/site-packages/fcache-0.1-py2.7.egg/fcache.py", line 163, in get
        if ((data[name]["expires"] is None) or
    KeyError: 'spanish'

Using the :meth:`~fcache.Cache.flush` method, you can clear all the data in a cache without deleting the cache file itself.

Delete a Cache
--------------

.. code-block:: python

    >>> import os.path
    >>> os.path.exists(cache.filename)
    True
    >>> cache.delete()
    >>> os.path.exists(cache.filename)
    False

The :func:`os.path.exists` function returns ``True`` if a file exists. In our case, we used it to show that the cache file does indeed exist. Then, we called the :meth:`~fcache.Cache.delete` method, which deletes the cache file.
