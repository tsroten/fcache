fcache
======

fcache is an easy-to-use file cache module for Python. It allows you to
interact with a filesystem cache like you would a dictionary. It also supports
data expiration, cache size management, and Python shelves.

.. code:: python

    >>> # Works like a dictionary:
    ... cache['foo'] = 'value'
    >>> cache['foo']
    'value'

    >>> # Store almost any Python object:
    ... cache['numbers'] = [1, 2, 3, 4, 5]

    >>> # Set data to expire:
    ... cache.set('chicago_weather', chicago_weather, 100)
    >>> cache['chicago_weather']
    '27 F, Partly Cloudy'
    >>> # Wait 100 seconds, then try again
    >>> cache['chicago_weather'] is None
    True

    >>> # Data is persistent
    ... exit()
    $ python
    >>> import fcache
    >>> cache = fcache.open('my_cache')
    >>> cache['foo']
    'value'

Install
-------

fcache supports Python 2.6, 2.7, and 3.

To install, use pip:

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
