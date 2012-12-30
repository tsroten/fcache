Introduction
============

This is the documentation for :mod:`fcache`. :mod:`fcache` is a Python module that provides a simple, persistent, file-based cache. Cached dated can optionally expire after a certain amount of time.

Prerequisites
-------------

:mod:`fcache` requires the `appdirs module <http://pypi.python.org/pypi/appdirs>`_ to work. :mod:`appdirs` is automatically installed using any of the installation methods listed below.

Installation
------------

There are multiple ways to install :mod:`fcache`. If you are confused about which method to use, try using ``pip``.

``pip`` (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`pip <http://www.pip-installer.org/>`_ is a tool for installing and managing Python packages. To install fcache, run:

.. code-block:: bash

    $ pip install fcache

This will download :mod:`fcache` from `the Python Package Index <http://pypi.python.org/>`_ and install it in your Python's ``site-packages`` directory.

Tarball Release
~~~~~~~~~~~~~~~

1. Download the most recent release from `fcache's PyPi page <http://pypi.python.org/pypi/fcache/>`_.
2. Unpack the tarball.
3. From inside the ``fcache-0.X`` directory, run ``python setup.py install``

This will install :mod:`fcache` in your Python's ``site-packages`` directory.

Install the Development Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`fcache's code <https://github.com/tsroten/fcache>`_ is hosted at GitHub. To install the development version, do the following:

1. Make sure `Git <http://git-scm.org/>`_ is installed. Test if it's installed by running ``git --version``
2. ``git clone git://github.com/tsroten/fcache.git``
3. ``pip install -e fcache``

This will link the ``fcache`` directory into your ``site-packages`` directory. You can find out where your ``site-packages`` directory is by running:

.. code-block:: bash

    python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"

Basic Usage
-----------

.. code-block:: python

    >>> import fcache
    >>> cache = fcache.Cache("population", "statistics-fetcher")
    >>> cache.set("chicago", 9729825)
    >>> print cache.get("chicago")
    9729825

This code creates the cache ``population`` for the application ``statistics-fetcher``. Then, it sets the key ``chicago`` to the value ``9729825``. Next, it prints the value of ``chicago``.
