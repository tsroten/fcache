Change Log
==========

v.0.6.0 (2024-11-19)
--------------------
* Allow multiple processes to safely call delete() at the same time. Thanks jacob-indigo!
* Remove EOL Python versions. Supporting only Python 3.9+

v.0.5.2 (2024-02-22)
--------------------

* Fix a race condition when multiple processes use the same file cache. Thanks dimitris-flyr!

v.0.5.1 (2023-06-28)
--------------------

* Switch from deprecated appdirs dependency to platformdirs.
* Restructure docs and add issue tracker/changes links to pypi.

v.0.5.0 (2023-03-19)
--------------------

* Do not catch OSError exceptions, so client code can handle and retry if needed. Fixes #27.
* Remove Python 2 support.
* Allow the chmod option to be set to False to disable file mode changes. Thanks morpheus65535!
* Adds context manager support. Thanks Yan Huihang!
* Exclude tests from installed package. Thanks ameyajoshi99!

v.0.4.7 (2017-03-11)
--------------------

* Minor code changes/updates.

v.0.4.6 (2017-01-30)
--------------------

* Allow app_cache_dir to be specified by user

v.0.4.5 (2015-10-21)
--------------------

* Uses shutil.move() instead of os.rename(). Fixes #22. Thanks Philip!
* Adds pypi and travis-ci badges to README.
* Adds flake8 to travis-ci and tox.
* Adds Python 3.5 tests.
* Includes tests in release package.

v.0.4.4 (2014-03-19)
--------------------

* Adds support for subcaches. Resolves #20.

v.0.4.3 (2014-03-13)
--------------------

* Creates AUTHORS.txt file.
* Adds test for FileCache.__iter__() and FileCache.__contains__().
* Fixes FileCache._all_keys assuming _buffer attribute (#19). Thanks soult!

v.0.4.2 (2014-03-01)
--------------------

* Adds unicode key support. Fixes #18.
* Adds docs test environment to tox. Fixes #17.
* Fixes code example typo. Fixes #16.
* Fixes typo in docstrings about serialization. Fixes #15.
* Adds not about appdirs requirement. Fixes #14.

v.0.4.1 (2014-01-03)
--------------------

* Adds appdirs support (issue #13)

v.0.4 (2014-01-02)
------------------

* backwards-incompatible rewrite; fcache now emulates a :class:`dict`.

v.0.3.1 (2013-04-19)
--------------------

* bug fix: close temp file after creation (issue #1)

v.0.3 (2013-01-03)
------------------

* now supports Python 2.6, 2.7, and 3.
* added :meth:`~fcache.Cache.set_default` method.
* :meth:`~fcache.Cache.invalidate` can now be called with no arguments, in which case it forces all data to expire.
* added :meth:`~fcache.Cache.keys` method.
* added :meth:`~fcache.Cache.values` method.
* added :meth:`~fcache.Cache.items` method.

v.0.2.1 (2012-12-31)
--------------------

* removed code-blocks from README so that PyPI would render the readme correctly.

v0.2 (2012-12-31)
-----------------

* added :meth:`~fcache.Cache.invalidate` method.
* added documentation.
* added *override* switch to the :meth:`~fcache.Cache.get` method.

v0.1 (2012-12-30)
-----------------

* Initial release.
