import codecs
import logging
import os
import pickle
import shutil
import tempfile

try:
    from collections.abc import MutableMapping
except ImportError:
    # Python 2 imports
    from collections import MutableMapping
    FileNotFoundError = IOError

from .posixemulation import rename

logger = logging.getLogger(__name__)


class FileCache(MutableMapping):
    """A persistent file cache that is dictionary-like and has a write buffer.

    By default, a write buffer is used, so writing to cache files is not done
    until :meth:`sync` is explicitly called. This behavior can be changed using
    the optional *flag* argument.

    .. NOTE::
        Keys and values are always stored as bytes. Keys are implicitly
        encoded to bytes before storage.

    """

    def __init__(self, cache_dir, flag='c', mode=0o666, keyencoding='utf-8',
                 serialize=True):
        """Initialize a :class:`FileCache` object.

        :param str cache_dir: The directory the cache will be stored in.
        :param flag: How the cache should be opened.
            First character ('r', 'w', 'c', or 'n'):
                'r': Open an existing cache in read-only mode.
                'w': Open an existing cache in read/write mode.
                'c': Open an existing cache in read/write mode or create a new
                    cache if one doesn't exist then open it for read/write.
                'n': Create a new cache even if one already exists, then open
                    it for read/write.
            Second character ('s'):
                's': Open the cache in sync mode. Writes are immediately
                    written to disk.
        :type flag: str (1-2 characters long)
        :param mode: The Unix mode for the cache files.
        :param str keyencoding: The encoding the keys use, defaults to 'utf-8'.
        :param bool serialize: Whether or not to (de)serialize the values.

        """
        if not isinstance(flag, str):
            raise TypeError("flag must be str not '%s'" % type(flag))
        elif flag[0] not in 'rwcn':
            raise ValueError("invalid flag: '%s', first flag must be one of "
                             "'r', 'w', 'c' or 'n'" % flag)
        elif len(flag) > 1 and flag[1] != 's':
            raise ValueError("invalid flag: '%s', second flag must be 's'" %
                             flag)
        if len(flag) > 1 and flag[1] == 's':
            self._sync = True
        else:
            self._sync = False
            self._buffer = {}
        self.cache_dir = cache_dir
        exists = os.path.exists(self.cache_dir)
        if exists and 'n' in flag:
            self.clear()
            self.create()
        elif not exists and ('c' in flag or 'n' in flag):
            self.create()
        elif not exists:
            raise FileNotFoundError("no such directory: '%s'" % cache_dir)
        self._flag = 'rb' if 'r' in flag else 'wb'
        self._mode = mode
        self._keyencoding = keyencoding
        self._serialize = serialize

    def create(self):
        """Create the write buffer and cache directory."""
        if not self._sync and not hasattr(self, '_buffer'):
            self._buffer = {}
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def clear(self):
        """Delete all write buffer items and cache files."""
        self.delete()
        self.create()

    def delete(self):
        """Delete the write buffer and cache directory."""
        if not self._sync:
            del self._buffer
        shutil.rmtree(self.cache_dir)

    def close(self):
        """Sync the write buffer, then close the cache."""
        self.sync()
        self.sync = self.create = self.delete = self._closed
        self._write_to_file = self._read_to_file = self._closed
        self._key_to_filename = self._filename_to_key = self._closed
        self.__getitem__ = self.__setitem__ = self.__delitem__ = self._closed
        self.__iter__ = self.__len__ = self.__contains__ = self._closed

    def sync(self):
        """Sync the write buffer with the cache files."""
        if self._sync:
            return  # opened in sync mode, so skip the manual sync
        self._sync = True
        for ekey in self._buffer:
            filename = self._key_to_filename(ekey)
            self._write_to_file(filename, self._buffer[ekey])
        self._buffer.clear()
        self._sync = False

    def _closed(self, *args, **kwargs):
        """Filler method for closed cache methods."""
        raise ValueError("invalid operation on closed cache")

    def _encode_key(self, key):
        """Encode key using hex_codec for constructing a cache filename.

        Keys are implicitly converted to bytes if passed as str.

        """
        if isinstance(key, str):
            key = key.encode(self._keyencoding)
        elif not isinstance(key, bytes):
            raise TypeError("key must be bytes or str")
        return codecs.encode(key, 'hex_codec').decode(self._keyencoding)

    def _decode_key(self, key):
        """Decode key using hex_codec to retrieve the original key."""
        return codecs.decode(key.encode(self._keyencoding), 'hex_codec')

    def _dumps(self, value):
        return value if not self._serialize else pickle.dumps(value)

    def _loads(self, value):
        return value if not self._serialize else pickle.loads(value)

    def _key_to_filename(self, key):
        """Convert an encoded key to an absolute cache filename."""
        return os.path.join(self.cache_dir, key)

    def _filename_to_key(self, absfilename):
        """Convert an absolute cache filename to an encoded key name."""
        return os.path.split(absfilename)[1]

    def _all_filenames(self):
        """Return a list of absolute cache filenames"""
        try:
            return [os.path.join(self.cache_dir, filename) for filename in
                    os.listdir(self.cache_dir)]
        except (FileNotFoundError, OSError):
            return []

    def _all_keys(self):
        """Return a list of all encoded key names."""
        file_keys = [self._filename_to_key(fn) for fn in self._all_filenames()]
        return set(file_keys + list(self._buffer))

    def _write_to_file(self, filename, bytesvalue):
        """Write bytesvalue to filename."""
        fh, tmp = tempfile.mkstemp()
        with os.fdopen(fh, self._flag) as f:
            f.write(self._dumps(bytesvalue))
        rename(tmp, filename)
        os.chmod(filename, self._mode)

    def _read_from_file(self, filename):
        """Read data from filename."""
        try:
            with open(filename, 'rb') as f:
                return self._loads(f.read())
        except (IOError, OSError):
            logger.warning('Error opening file: %s' % filename)
            return None

    def __setitem__(self, key, value):
        ekey = self._encode_key(key)
        if not self._sync:
            self._buffer[ekey] = value
        else:
            filename = self._key_to_filename(ekey)
            self._write_to_file(filename, value)

    def __getitem__(self, key):
        ekey = self._encode_key(key)
        if not self._sync:
            try:
                return self._buffer[ekey]
            except KeyError:
                pass
        filename = self._key_to_filename(ekey)
        if not filename in self._all_filenames():
            raise KeyError(key)
        return self._read_from_file(filename)

    def __delitem__(self, key):
        ekey = self._encode_key(key)
        filename = self._key_to_filename(ekey)
        if not self._sync:
            try:
                del self._buffer[ekey]
            except KeyError:
                if not filename in self._all_filenames():
                    raise KeyError(key)
        try:
            os.remove(filename)
        except (IOError, OSError):
            pass

    def __iter__(self):
        for key in self._all_keys():
            yield self._decode_key(key)

    def __len__(self):
        return len(self._all_keys())

    def __contains__(self, key):
        ekey = self._encode_key(key)
        return ekey in self._all_keys()
