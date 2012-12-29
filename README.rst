fcache
======

About
-----

fcache is a simple file-based cache module for Python. It stores cache files in OS-appropriate, application-specific cache directories. Cached data can optionally be set to expire after a certain amount of time. fcache can store any data supported by the `cPickle module <http://docs.python.org/2/library/pickle.html#module-cPickle>`_.

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

    >>> from fcache import Cache
    >>> cache = Cache("weather", "fetchweather", "Joe Developer")
    >>> cache.set("nyc", nyc_weather, 60 * 60)

We just created a new cache named "weather" for the "fetchweather" application, which was written by "Joe Developer" (application-specific cache directories on Windows use the developer's name). Then, we put the current weather into the cache under the key "nyc" for 1 hour. We can fetch the data for the next hour; after that, it expires.

30 minutes later, you already forgot what the weather is. Let's retrieve the data::

    >>> from fcache import Cache
    >>> cache = Cache("weather", "fetchweather", "Joe Developer")
    >>> cache.get("nyc")
    {'temp': '77', 'conditions': 'cloudy'}

This time, when we created a Cache object with the name "weather", fcache recognized that there was already an associated cache file, so it read that file instead of creating a new one.

Removing Data
~~~~~~~~~~~~~

Now that you've checked the weather, you've decided you don't need to store New York's weather data any longer::

    >>> from fcache import Cache
    >>> cache = Cache("weather", "fetchweather", "Joe Developer")
    >>> cache.remove("nyc")
    True

A True return value means that the data was located and deleted.

**NOTE**: the "weather" cache still exists and can be used to save more data -- only the "nyc" data was deleted.

Deleting a Cache
~~~~~~~~~~~~~~~~

Let's say you're finished caching weather data altogether and want to delete your "weather" cache::

    >>> from fcache import Cache
    >>> cache = Cache("weather", "fetchweather", "Joe Developer")
    >>> cache.delete()
    True

A True return value means the cache file was deleted from the file system. All data inside the "weather" cache is now gone.

Cache Directory Location
------------------------

fcache uses the `appdirs module's <http://pypi.python.org/pypi/appdirs>`_ "user_cache_dir" method to determine where to store cache files.
