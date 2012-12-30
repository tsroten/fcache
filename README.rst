fcache
======

About
-----

fcache is a simple file-based cache module for Python. It stores cache files in OS-appropriate, application-specific cache directories. Cached data can optionally expire after a certain amount of time. fcache can store any data supported by the `pickle module <http://docs.python.org/2/library/pickle.html>`_. fcache uses the `appdirs module's <http://pypi.python.org/pypi/appdirs>`_ "user_cache_dir" method to determine where to store cache files.

Installation
------------

Install using pip::

    pip install fcache

Usage
-----

Setting and Getting Data
~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you just fetched some weather data that you want to cache for the next hour::

    >>> nyc_weather = {"temp": "77", "conditions": "cloudy"}

Let's store the data using fcache::

    >>> import fcache
    >>> cache = fcache.Cache("weather", "fetchweather")
    >>> cache.set("nyc", nyc_weather, 60 * 60)

We just created a new cache named "weather" for the "fetchweather" application. Then, we put the current weather into the cache under the key "nyc" for 1 hour. We can fetch the data for the next hour; after that, it expires.

30 minutes later, you already forgot what the weather is. Let's retrieve the data::

    >>> cache.get("nyc")
    {'temp': '77', 'conditions': 'cloudy'}

Removing Data
~~~~~~~~~~~~~

Now that you've checked the weather, you've decided you don't need to store New York's weather data any longer::

    >>> cache.remove("nyc")

**NOTE**: the "weather" cache still exists and can be used to save more data -- only the "nyc" data was deleted.

Flushing a Cache
~~~~~~~~~~~~~~~~

Perhaps you've spent all afternoon gathering weather data and storing it in your cache. But, now you want to flush all the data in anticipation for tomorrow's data. In other words, you want to remove the data, but not remove the cache file itself::

    >>> cache.flush()

Deleting a Cache
~~~~~~~~~~~~~~~~

Let's say you're finished caching weather data altogether and want to delete your "weather" cache file::

    >>> cache.delete()

License
-------

fcache is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
