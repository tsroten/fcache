import os
import sys
import unittest

is_py3 = sys.version_info[0] > 2

if is_py3:
    from io import UnsupportedOperation
else:
    FileNotFoundError = IOError
    UnsupportedOperation = IOError

import fcache.cache as fcache


class TestFileCache(unittest.TestCase):

    def setUp(self):
        self.cache_dir = 'test_cache'
        self.cache = fcache.FileCache(self.cache_dir)

    def tearDown(self):
        try:
            self.cache.delete()
        except (ValueError, FileNotFoundError, OSError):
            pass

    def test_init(self):
        self.assertTrue(os.path.exists(self.cache_dir))
        self.assertEqual(self.cache.cache_dir, self.cache_dir)
        self.assertEqual(self.cache._flag, 'wb')
        self.assertEqual(self.cache._keyencoding, 'utf-8')
        self.assertFalse(self.cache._sync)
        self.assertEqual(self.cache._buffer, {})
        self.assertEqual(self.cache._mode, 0o666)
        self.cache.close()
        self.cache = fcache.FileCache(self.cache_dir, flag='ws')
        self.assertTrue(self.cache._sync)
        self.assertFalse(hasattr(self.cache, '_buffer'))

        # test flag validation
        self.assertRaises(TypeError, fcache.FileCache, self.cache_dir, 1)
        self.assertRaises(ValueError, fcache.FileCache, self.cache_dir, 'z')
        self.assertRaises(ValueError, fcache.FileCache, self.cache_dir, 'rz')

    def test_delete_create(self):
        self.assertTrue(os.path.exists(self.cache_dir))
        self.cache.delete()
        self.assertFalse(os.path.exists(self.cache_dir))
        self.assertFalse(hasattr(self.cache, '_buffer'))
        self.cache.create()
        self.assertTrue(os.path.exists(self.cache_dir))
        self.assertTrue(hasattr(self.cache, '_buffer'))

    def test_clear(self):
        self.cache['foo'] = b'value'
        self.cache.sync()
        self.cache['bar'] = b'value'
        self.cache.clear()
        self.assertTrue(os.path.exists(self.cache_dir))
        self.assertRaises(KeyError, self.cache.__getitem__, 'foo')
        self.assertRaises(KeyError, self.cache.__getitem__, 'bar')

    def test_sync(self):
        self.cache['foo'] = b'value'
        self.assertFalse(os.path.exists(self.cache._key_to_filename(
            self.cache._encode_key('foo'))))
        self.assertTrue(self.cache._encode_key('foo') in self.cache._buffer)
        self.cache.sync()
        self.assertTrue(os.path.exists(self.cache._key_to_filename(
            self.cache._encode_key('foo'))))
        self.assertFalse(self.cache._encode_key('foo') in self.cache._buffer)
        self.cache.clear()
        self.cache = fcache.FileCache(self.cache_dir, flag='cs')
        self.cache['foo'] = b'value'
        self.assertTrue(os.path.exists(self.cache._key_to_filename(
            self.cache._encode_key('foo'))))

    def test_close(self):
        self.cache.close()
        self.assertRaises(ValueError, self.cache.create)
        self.assertRaises(ValueError, self.cache.sync)
        self.assertRaises(ValueError, self.cache.delete)
        self.assertRaises(ValueError, self.cache.close)
        self.assertRaises(ValueError, self.cache.clear)
        self.assertRaises(ValueError, self.cache.__len__)
        self.assertRaises(ValueError, self.cache.__iter__)
        self.assertRaises(ValueError, self.cache.__contains__)
        self.assertRaises(ValueError, self.cache.__getitem__)
        self.assertRaises(ValueError, self.cache.__setitem__)
        self.assertRaises(ValueError, self.cache.__delitem__)
        self.assertEqual(self.cache._flag, None)
        self.assertEqual(self.cache._mode, None)
        self.assertEqual(self.cache._keyencoding, None)
        self.assertEqual(self.cache.cache_dir, None)
        self.assertEqual(self.cache._sync, None)
        self.assertEqual(self.cache._buffer, None)

    def test_flag(self):
        self.cache.delete()
        self.assertRaises(FileNotFoundError, fcache.FileCache,
                          self.cache_dir, flag='r')
        self.assertRaises(FileNotFoundError, fcache.FileCache,
                          self.cache_dir, flag='w')
        self.cache = fcache.FileCache(self.cache_dir, flag='ns')
        self.assertTrue(os.path.exists(self.cache_dir))
        self.cache['foo'] = b'value'
        self.cache = fcache.FileCache(self.cache_dir, flag='n')
        self.assertEqual(len(self.cache), 0)
        self.cache = fcache.FileCache(self.cache_dir, flag='rs')
        self.assertRaises(UnsupportedOperation, self.cache.__setitem__,
                          'foo', b'value')

    def test_key_encode_decode(self):
        skey = 'foo'
        skey_hex = '666f6f'
        bkey = skey.encode('utf-8')
        self.assertEqual(self.cache._encode_key(bkey), skey_hex)
        self.assertEqual(self.cache._encode_key(skey), skey_hex)
        self.assertEqual(self.cache._decode_key(skey_hex), bkey)
        self.assertRaises(TypeError, self.cache._encode_key, 1)

    def test_delitem(self):
        self.cache['a'] = b'1'
        self.assertEqual(self.cache['a'], b'1')
        del self.cache['a']
        self.assertFalse('a' in self.cache)


if __name__ == '__main__':
    unittest.main()
