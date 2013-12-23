"""Provides mixins that are useful with mutable mapping containers or Shelves.

Classes:
    LRUMixin: Add LRU data management to mutable mapping containers.
    LRUDict: A Python dictionary with LRU data management.
    LRUShelf: A Shelf with LRU data management.
    TimeoutMixin: Add data timeout to mutable mapping containers.
    TimeoutDict: A Python dictionary with data timeout features.
    TimeoutShelf: A Shelf with data timeout features.
    LRUTimeoutShelf: A Shelf with LRU data management and data timeout.

Functions:
    open: Open a dbm file for writing using LRUTimeoutShelf.

"""
from collections import deque
from pickle import HIGHEST_PROTOCOL
from shelve import Shelf
import sys
from time import time

is_py3 = sys.version_info[0] > 2

if is_py3:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping

DEFAULT_MAXSIZE = 300
DEFAULT_TIMEOUT = 0


class LRUMixin(object):
    """Add LRU data management to mutable mapping containers, e.g. Shelf.

    This mixin will keep a mutable mapping container under a given length by
    discarding the least recently used items when the container overflows.
    This is helpful if you have a cache that should stay under a certain size
    due to performance/memory concerns.

    Note: The queue that keeps track of which keys are the most least recently
    used is not persistent.

    For this mixin to work well, all dict methods that involve setting a key,
    getting a value, or deleting a key need to be routed through this class'
    __setitem__, __getitem__, and __delitem__. The built-in dict class won't do
    this by default, so it is better to inherit from UserDict if you want to
    make a custom dictionary. If you subclass dict, you might want to also
    inherit from MutableMapping so the LRUMixin will work properly. Otherwise,
    you will need to manually code methods such as update(), copy(), keys(),
    values(), etc. So, it's best to stick with MutableMapping or UserDict if
    possible.

    """

    def __init__(self, *args, **kwargs):
        """Initialize LRU data management for a mapping container.

        Keyword arguments:
            maxsize: The maximum size the container should be. Defaults to
                module-level DEFAULT_MAXSIZE.

        """
        self.maxsize = kwargs.get('maxsize', DEFAULT_MAXSIZE)
        if 'maxsize' in kwargs:
            del kwargs['maxsize']
        super(LRUMixin, self).__init__(*args, **kwargs)
        self._queue = deque()  # linked list of keys
        for key in list(self.keys()):  # populate linked list
            self._remove_add_key(key)

    def _remove_add_key(self, key):
        """Move a key to the end of the linked list and discard old entries."""
        if not hasattr(self, '_queue'):
            return  # haven't initialized yet, so don't bother
        if key in self._queue:
            self._queue.remove(key)
        self._queue.append(key)
        while len(self._queue) > self.maxsize:
            del self[self._queue[0]]

    def __getitem__(self, key):
        value = super(LRUMixin, self).__getitem__(key)
        self._remove_add_key(key)
        return value

    def __setitem__(self, key, value):
        super(LRUMixin, self).__setitem__(key, value)
        self._remove_add_key(key)

    def __delitem__(self, key):
        super(LRUMixin, self).__delitem__(key)
        if hasattr(self, '_queue'):
            self._queue.remove(key)


class TimeoutMixin(object):
    """Add data timeout to mapping containers.

    If you try to access an expired key, a KeyError will be raised, just like
    when you try to access a non-existent key.

    For this mixin to work well, all dict methods that involve setting a key,
    getting a value, deleting a key, iterating over the container, or getting
    the length or formal representation need to be routed through this class'
    __setitem__, __getitem__, __delitem__, __iter__, __len__, and __repr__.
    The built-in dict class won't do this by default, so it is better to
    inherit from UserDict if you want to make a custom dictionary. If you
    subclass dict, you might want to also inherit from MutableMapping so the
    TimeoutMixin will work properly. Otherwise, you will need to manually
    code methods such as update(), copy(), keys(), values(), etc. So, it's
    best to stick with MutableMapping or UserDict if possible.

    Attributes:
        default_timeout: The default timeout value in seconds.
            A zero means that keys won't timeout by default.
        _index: The timeout index mapping (maps keys to timeout values).
        _INDEX: The key name used for the timeout index.

    """

    _INDEX = 'f1dd04ff3d4d9adfabd43a3f9fda9b4b78302b21'

    def __init__(self, *args, **kwargs):
        """Initialize the timeout features of the mapping container.

        After calling the base class' __init__() method, the timeout index
        is read from the container or created if it doesn't exist. Then, any
        existing expired values are deleted.

        Keyword arguments:
            default_timeout: The default timeout value in seconds to use. If
                not present, the module-level constant DEFAULT_TIMEOUT value
                is used.

        """
        try:
            self.default_timeout = kwargs.pop('default_timeout')
        except KeyError:
            self.default_timeout = DEFAULT_TIMEOUT
        super(TimeoutMixin, self).__init__(*args, **kwargs)
        try:
            self._index = super(TimeoutMixin, self).__getitem__(self._INDEX)
        except KeyError:
            self._index = {}
            super(TimeoutMixin, self).__setitem__(self._INDEX, self._index)
        else:
            for key in self:
                self._is_expired(key)
        self._skey = object()  # used for self.set()

    def _is_expired(self, key):
        """Check if a key is expired. If so, delete the key."""
        if not hasattr(self, '_index'):
            return False  # haven't initalized yet, so don't bother
        timeout = self._index[key]
        if timeout is None or timeout >= time():
            return False
        del self[key]  # key expired, so delete it from container
        return True

    def __getitem__(self, key):
        if key == self._INDEX:
            raise KeyError("cannot access protected key '%s'" % self._INDEX)
        try:
            if not self._is_expired(key):
                return super(TimeoutMixin, self).__getitem__(key)
        except KeyError:
            pass
        raise KeyError(key)

    def set(self, key, value, timeout=None):
        """Set a key with a timeout value (in seconds).

        Recoginzed timeout values:
            non-zero integer: Number of seconds until the key should expire.
            0: The key will never expire.
            None: The class' default_timeout value is used.

        """
        if key == self._INDEX:
            raise TypeError("reserved key name '%s'" % self._INDEX)
        self[key] = value
        if hasattr(self, '_index'):  # check if __init__ completed
            self._skey = key  # let __setitem__() know the key we are storing
            timeout = timeout if timeout is not None else self.default_timeout
            self._index[key] = int(time() + timeout) if timeout else None
            self._skey = object()

    def __setitem__(self, key, value):
        if key == self._INDEX:
            raise TypeError("reserved key name '%s'" % self._INDEX)
        super(TimeoutMixin, self).__setitem__(key, value)
        if self._skey != key and hasattr(self, '_index'):
            # the key we are storing doesn't match _skey, so update index
            timeout = self.default_timeout
            self._index[key] = int(time() + timeout) if timeout else None

    def __delitem__(self, key):
        if key == self._INDEX:
            raise KeyError("cannot delete protected key '%s'" % self._INDEX)
        super(TimeoutMixin, self).__delitem__(key)
        if hasattr(self, '_index'):  # check if __init__ completed
            del self._index[key]

    def __iter__(self):
        for key in super(TimeoutMixin, self).__iter__():
            if key == self._INDEX:
                continue
            if not self._is_expired(key):
                yield key

    def __contains__(self, key):
        if key == self._INDEX:
            return False
        return super(TimeoutMixin, self).__contains__(key)

    def __len__(self):
        return super(TimeoutMixin, self).__len__() - 1  # hide the index

    def __repr__(self):
        for key in self:  # delete expired data via __iter__()
            pass
        super(TimeoutMixin, self).__delitem__(self._INDEX)  # hide the index
        _repr = super(TimeoutMixin, self).__repr__()
        super(TimeoutMixin, self).__setitem__(self._INDEX, self._index)
        return _repr

    def sync(self):
        super(TimeoutMixin, self).__setitem__(self._INDEX, self._index)
        super(TimeoutMixin, self).sync()

    def __del__(self):
        """Sync index when __del__ is called"""
        super(TimeoutMixin, self).__setitem__(self._INDEX, self._index)
        super(TimeoutMixin, self).__del__()

    def __exit__(self, *exc_info):
        self.sync()
        super(TimeoutMixin, self).__exit__(*exc_info)


class _NewOldMixin(object):
    """Makes certain dict methods follow MRO to the container."""

    def __init__(self, *args, **kwargs):
        self._class = kwargs.pop('old_class')
        self._class.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        return self._class.__getitem__(self, key)

    def __setitem__(self, key, value):
        return self._class.__setitem__(self, key, value)

    def __delitem__(self, key):
        return self._class.__delitem__(self, key)

    def __iter__(self):
        return self._class.__iter__(self)

    def __len__(self):
        return self._class.__len__(self)


class LRUDict(LRUMixin, _NewOldMixin, MutableMapping, dict):
    """A Python dictionary with LRU data management."""

    def __init__(self, *args, **kwargs):
        super(LRUDict, self).__init__(*args, old_class=dict, **kwargs)


class TimeoutDict(TimeoutMixin, _NewOldMixin, MutableMapping, dict):
    """A Python dictionary with data timeout."""

    def __init__(self, *args, **kwargs):
        super(TimeoutDict, self).__init__(*args, old_class=dict, **kwargs)


class LRUTimeoutDict(LRUMixin, TimeoutMixin, _NewOldMixin, MutableMapping,
                     dict):
    """A Python dictionary with LRU data management and data timeout."""

    def __init__(self, *args, **kwargs):
        super(LRUTimeoutDict, self).__init__(*args, old_class=dict, **kwargs)


class LRUShelf(LRUMixin, _NewOldMixin, Shelf):
    """A Shelf with LRU data management."""

    def __init__(self, *args, **kwargs):
        super(LRUShelf, self).__init__(*args, old_class=Shelf, **kwargs)


class TimeoutShelf(TimeoutMixin, _NewOldMixin, Shelf):
    """A Shelf with data timeout."""

    def __init__(self, *args, **kwargs):
        super(TimeoutShelf, self).__init__(*args, old_class=Shelf, **kwargs)

    if not is_py3:
        def keys(self):
            """Override Shelf's keys() so we can hide the timeout index."""
            _keys = self.dict.keys()
            if self._INDEX in _keys:
                _keys.remove(self._INDEX)
            keys = []
            for key in _keys:
                if not self._is_expired(key):
                    keys.append(key)
            return _keys


class LRUTimeoutShelf(LRUMixin, TimeoutShelf):
    """A Shelf with LRU data management and data timeout."""

    def __init__(self, *args, **kwargs):
        super(LRUTimeoutShelf, self).__init__(*args, **kwargs)


def open(filename, flag='c', protocol=HIGHEST_PROTOCOL, writeback=False,
         keyencoding='utf-8', maxsize=DEFAULT_MAXSIZE,
         default_timeout=DEFAULT_TIMEOUT):
    """Open a dbm file for writing using LRUTimeoutShelf.

    Arguments:
        filename: The base filename for the underlying database.
        flag: See dbm.open()'s documentation. Default is 'c', which means to
            open an existing database for r/w or create a new one if none
            exists.
        protocol: The pickle protocol to use. Default to the highest protocol.
        writeback: Make Shelf keep a cache of the entries and rewrite on close.
        keyencoding: The encoding to use for the keys (Python 3 only).
        maxsize: The maxsize the cache should be allowed to grow to.
        default_timeout: The default timeout value (in seconds).

    """
    import dbm
    dict = dbm.open(filename, flag)
    if is_py3:
        shelf = LRUTimeoutShelf(dict, protocol, writeback, keyencoding,
                                default_timeout=default_timeout,
                                maxsize=maxsize)
    else:
        shelf = LRUTimeoutShelf(dict, protocol, writeback,
                                default_timeout=default_timeout,
                                maxsize=maxsize)
    return shelf
