import os
import sys
import time
import unittest

is_py3 = sys.version_info[0] > 2

if is_py3:
    from collections.abc import Iterable, MappingView
else:
    from collections import Iterable, MappingView

import fcache.cache as cache
import fcache.shelf as fcache


class TestLRUMixin(unittest.TestCase):

    def setUp(self):
        self.dict = fcache.LRUDict()

    def test_init(self):
        self.assertTrue(hasattr(self.dict, 'maxsize'))
        self.assertTrue(hasattr(self.dict, '_queue'))

    def test_remove_add_key(self):
        self.dict['a'] = 1
        self.dict['b'] = 2
        self.dict['c'] = 3
        self.assertEqual(list(self.dict._queue), ['a', 'b', 'c'])
        self.dict._remove_add_key('b')
        self.assertEqual(list(self.dict._queue), ['a', 'c', 'b'])
        self.dict._remove_add_key('a')
        self.assertEqual(list(self.dict._queue), ['c', 'b', 'a'])
        self.dict._remove_add_key('d')
        self.assertEqual(list(self.dict._queue), ['c', 'b', 'a', 'd'])
        self.dict = fcache.LRUDict({'a': 1, 'b': 2, 'c': 3, 'd': 4}, maxsize=3)
        self.assertEqual(len(self.dict), 3)

    def test_setitem(self):
        self.dict['a'] = 1
        self.dict['b'] = 2
        self.dict.maxsize = 3
        self.dict.update({'c': 3, 'd': 4})
        self.assertEqual(len(self.dict), 3)

    def test_delitem(self):
        self.dict['a'] = 1
        self.assertEqual(len(self.dict), len(self.dict._queue))
        del self.dict['a']
        self.assertEqual(len(self.dict), len(self.dict._queue))


class TestTimeoutMixin(unittest.TestCase):

    def setUp(self):
        self.dict = fcache.TimeoutDict()

    def test_index_unchangeable_and_invisible(self):
        self.assertRaises(TypeError, self.dict.set, self.dict._INDEX, 'blah')
        self.assertRaises(TypeError, self.dict.__setitem__, self.dict._INDEX,
                          'blah')
        self.assertRaises(KeyError, self.dict.__delitem__, self.dict._INDEX)
        self.assertTrue(self.dict._INDEX not in list(self.dict.keys()))
        self.assertTrue(self.dict._INDEX not in repr(self.dict))
        self.assertEqual(len(self.dict), 0)

    def test_timeout(self):
        self.dict.set('foo', 'value', 1)
        self.assertEqual(self.dict['foo'], 'value')
        time.sleep(1)
        self.assertRaises(KeyError, self.dict.__getitem__, 'foo')
        self.assertEqual(self.dict.get('foo', 'blah'), 'blah')

    def test_default_timeout(self):
        self.dict.default_timeout = 1
        self.dict['foo'] = 'value'
        self.assertEqual(self.dict['foo'], 'value')
        time.sleep(1)
        self.assertRaises(KeyError, self.dict.__getitem__, 'foo')


class TestDictMethods(unittest.TestCase):

    classes = [fcache.LRUDict, fcache.TimeoutDict,
               fcache.LRUTimeoutDict, fcache.LRUShelf,
               fcache.TimeoutShelf, fcache.LRUTimeoutShelf]
    shelves = [fcache.LRUShelf, fcache.TimeoutShelf, fcache.LRUTimeoutShelf]

    def delete_cache_files(self):
        if os.path.exists('test_cache'):
            os.remove('test_cache')
        if os.path.exists('test_cache.db'):
            os.remove('test_cache.db')

    def test_classes(self):
        for _class in self.classes:
            obj = _class(dict() if 'Shelf' in str(_class) else '')
            if 'LRU' in str(_class):
                self.lru_methods(obj)
            obj = _class(dict() if 'Shelf' in str(_class) else '')
            if 'Timeout' in str(_class):
                self.timeout_methods(obj)
            obj = _class(dict() if 'Shelf' in str(_class) else '')
            if 'LRU' in str(_class) and 'Timeout' in str(_class):
                self.lru_timeout_methods(obj)

        for shelf in self.shelves:
            obj = shelf(cache.FileCache('test_cache'))
            if 'LRU' in str(shelf):
                self.lru_methods(obj)
            obj.dict.delete()
            obj = shelf(cache.FileCache('test_cache'))
            if 'Timeout' in str(shelf):
                self.timeout_methods(obj)
            obj.dict.delete()
            obj = shelf(cache.FileCache('test_cache'))
            if 'LRU' in str(shelf) and 'Timeout' in str(shelf):
                self.lru_timeout_methods(obj)
            obj.dict.delete()

    def basic_access_methods(self, obj):
        """Tests __setitem__, __getitem__, __delitem___, __contains__,
        and __len__.

        """
        obj['a'] = 1
        self.assertTrue('a' in obj)
        self.assertEqual(obj['a'], 1)
        self.assertEqual(len(obj), 1)
        del obj['a']
        self.assertFalse('a' in obj)
        self.assertRaises(KeyError, obj.__getitem__, 'a')
        self.assertEqual(len(obj), 0)

    def advanced_access_methods(self, obj):
        """Tests get(), setdefault(), update(), pop(), popitem(), and
        clear().

        """
        self.assertEqual(obj.get('a', 'blah'), 'blah')
        self.assertEqual(obj.setdefault('a', 'blah'), 'blah')
        obj.update({'b': 2, 'c': 3, 'd': 4})
        self.assertEqual(obj.get('b'), 2)
        self.assertEqual(len(obj), 4)
        self.assertEqual(obj.pop('a'), 'blah')
        self.assertRaises(KeyError, obj.pop, 'a')
        self.assertEqual(type(obj.popitem()), tuple)
        self.assertEqual(len(obj), 2)
        obj.clear()
        self.assertEqual(len(obj), 0)

    def iter_view_methods(self, obj):
        self.assertTrue(isinstance(obj.__iter__(), Iterable))
        self.assertTrue(isinstance(obj.items(),
                        MappingView if is_py3 else list))
        self.assertTrue(isinstance(obj.keys(),
                        MappingView if is_py3 else list))
        self.assertTrue(isinstance(obj.values(),
                        MappingView if is_py3 else list))
        if not is_py3:
            self.assertTrue(isinstance(obj.iteritems(), Iterable))
            self.assertTrue(isinstance(obj.iterkeys(), Iterable))
            self.assertTrue(isinstance(obj.itervalues(), Iterable))
            self.assertTrue(isinstance(obj.viewitems(), MappingView))
            self.assertTrue(isinstance(obj.viewkeys(), MappingView))
            self.assertTrue(isinstance(obj.viewvalues(), MappingView))

    def lru_methods(self, obj):
        pass

    def timeout_methods(self, obj):
        self.assertTrue(obj._INDEX not in obj)

    def lru_timeout_methods(self, obj):
        obj.maxsize = 3
        obj.default_timeout = 1
        obj['a'], obj['b'] = 1, 2
        self.assertEqual((obj['a'], obj['b']), (1, 2))
        time.sleep(1)
        self.assertRaises(KeyError, obj.__getitem__, 'b')
        obj.default_timeout = 0
        obj['a'], obj['b'], obj['c'] = 1, 2, 3
        self.assertEqual(len(obj), 3)
        obj['d'] = 4
        self.assertEqual(len(obj), 3)
        self.assertRaises(KeyError, obj.__getitem__, 'a')


if __name__ == '__main__':
    unittest.main()
