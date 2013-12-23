import codecs
import logging
import os
import shutil
import tempfile

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
    FileNotFoundError = IOError

from .posixemulation import rename

logger = logging.getLogger(__name__)


def _closed():
    raise ValueError("invalid operation on closed cache")


class FileCache(MutableMapping):
    """A persistent file cache that is shelve.Shelf-compatible and dict-like.

    By default, a write buffer is used and writing to cache files is not done
    until sync is explicitly called. This behavior can be changed using the
    optional flag argument.

    Note: Keys and values are always stored as bytes. Keys are implicitly
    encoded to bytes before storage.

    Note: This class does not serialize/deserialize data. The shelve.Shelf
    class provides a good wrapper for that.

    *This cache is not meant to be used directly, but with an interface like
    Shelf.*

    Methods:
        clear: Delete all write buffer items and cache files.
        close: Sync the write buffer, then close the cache.
        create: Create the write buffer and cache directory.
        delete: Delete the write buffer and cache directory.
        sync: Sync the write buffer with the cache files.

    """

    def __init__(self, cache_dir, flag='c', mode=0o666, keyencoding='utf-8'):
        """Initialize a FileCache object.

        Arguments:
            cache_dir: The directory the cache will be stored in.
            flag: How the cache should be opened (1-2 character string).
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
            mode: The Unix mode for the cache files.
            keyencoding: The encoding the keys use.

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
            raise FileNotFoundError('No such directory: %s' % cache_dir)
        self._flag = 'rb' if 'r' in flag else 'wb'
        self._mode = mode
        self._keyencoding = keyencoding

    def _encode_key(self, key):
        """Encode key using hex_codec for constructing a cache filename.

        Keys are implicitly converted to bytes if passed as str.

        """
        if isinstance(key, str):
            key = key.encode(self._keyencoding)
        elif not isinstance(key, bytes):
            raise TypeError('Key must be bytes or str')
        return codecs.encode(key, 'hex_codec').decode(self._keyencoding)

    def _decode_key(self, key):
        """Decode key using hex_codec to retrieve the original key."""
        return codecs.decode(key.encode(self._keyencoding), 'hex_codec')

    def create(self):
        """Create the write buffer and cache directory."""
        if not self._sync:
            self._buffer = {}
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

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
        self._flag = self._mode = self._keyencoding = None
        self.cache_dir = self._sync = self._buffer = None
        self.delete = self.sync = self.clear = self.create = _closed
        self.__delitem__ = self.__getitem__ = self.__setitem__ = _closed
        self.__iter__ = self.__len__ = self.__contains__ = _closed

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

    def _write_to_file(self, filename, bytesvalue):
        """Write bytesvalue to filename."""
        fh, tmp = tempfile.mkstemp()
        with os.fdopen(fh, self._flag) as f:
            f.write(bytesvalue)
        rename(tmp, filename)
        os.chmod(filename, self._mode)

    def _read_from_file(self, filename):
        """Read data from filename."""
        try:
            with open(filename, 'rb') as f:
                return f.read()
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
            raise KeyError('Key Error: %s' % key)
        return self._read_from_file(filename)

    def __delitem__(self, key):
        ekey = self._encode_key(key)
        filename = self._key_to_filename(ekey)
        if not self._sync:
            try:
                del self._buffer[ekey]
            except KeyError:
                if not filename in self._all_filenames():
                    raise KeyError('Key Error: %s' % key)
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

    def __del__(self):
        if not hasattr(self, '_buffer') or self._sync is None:
            return  # cache is deleted or cache is closed, so don't sync
        self.sync()
