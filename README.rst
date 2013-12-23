Tick Tock
=========

Tick Tock adds useful features to Python's ``Shelf`` class. Specifically, Tick Tock
adds data expiration and least-recently-used (LRU) cache management. Tick Tock also
provides mixins that can be used with any dictionary-like container, not just
shelves. Lastly, Tick Tock provides a cross-platform file-based backend to
replace ``dbm.dumb`` when creating a ``Shelf``.

.. code:: python

    >>> # Make your shelves manage your data based on time and size:
    ... shelf = ticktock.open('cache_dir', timeout=60, maxsize=50)

    >>> shelf['foo'] = 'value'
    >>> shelf['foo']
    'value'
    >>> # Wait 60 seconds, then try again:
    ... shelf['foo']
        ...
        KeyError: 'foo'
    
    >>> len(shelf)
    50
    >>> shelf['bar'] = 'value'
    >>> # Adding 'bar' kicks the least-recently-used key out of the Shelf
    ... len(shelf)
    50

Class list:
    * LRUShelf - a Shelf with LRU size management
    * TimeoutShelf - a Shelf with data expiration
    * LRUTimeoutShelf - a Shelf with LRU size management and data expiration
    * LRUMixin - add LRU size management to dictionary-like container classes
    * TimeoutMixin - add data expiration to dictionary-like container classes
    * TimeoutDict - a dictionary with data expiration
    * LRUDict - a dictionary with LRU size management
    * LRUTimeoutDict - a dictionary with LRU size management and data expiration
    * FileCache - a file-based container that uses a write buffer and separate
      files for each value

Install
-------

Tick Tock supports Python 2.6, 2.7, and 3.

To install, use pip:

.. code:: bash

    $ pip install ticktock

Documentation
-------------

`Tick Tock's documentation <https://ticktock.readthedocs.org/>`_ contains an introduction along with an API overview. For more information on how to get started with Tick Tock, be sure to read the documentation.

Bug/Issues Tracker
------------------

Tick Tock uses its `GitHub Issues page <https://github.com/tsroten/ticktock/issues>`_ to track bugs, feature requests, and support questions.

License
-------

Tick Tock is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
