import os
import time
import unittest

import fcache


class testCache(unittest.TestCase):

    def setUp(self):
        self.cache = fcache.Cache("unittest", "fcache")
        self.cache.set("n", 43)
        self.cache.set("timer", 1, 1)

    def tearDown(self):
        if os.access(self.cache.filename, os.F_OK) is True:
            self.cache.delete()
        self.cache = None

    def test_init(self):
        self.assertTrue(os.access(self.cache.filename, os.F_OK))

    def test_set(self):
        self.cache.delete()
        self.assertRaises(IOError, self.cache.set, "n", 43)

    def test_get(self):
        self.assertEqual(self.cache.get("n"), 43)
        self.assertEqual(self.cache.get("timer"), 1)
        time.sleep(1)
        self.assertEqual(self.cache.get("timer"), None)
        self.assertEqual(self.cache.get("timer", True), 1)
        self.assertRaises(KeyError, self.cache.get, "j")
        self.cache.delete()
        self.assertRaises(IOError, self.cache.get, "j")

    def test_invalidate(self):
        self.assertEqual(self.cache.get("n"), 43)
        self.cache.invalidate("n")
        self.assertEqual(self.cache.get("n"), None)
        self.assertRaises(KeyError, self.cache.invalidate, "j")
        self.cache.delete()
        self.assertRaises(IOError, self.cache.invalidate, "n")

    def test_remove(self):
        self.cache.remove("n")
        self.assertRaises(KeyError, self.cache.get, "n")
        self.assertRaises(KeyError, self.cache.remove, "j")
        self.cache.delete()
        self.assertRaises(IOError, self.cache.remove, "j")

    def test_flush(self):
        self.cache.flush()
        self.assertEqual(self.cache._read(), {})

    def test_delete(self):
        self.cache.delete()
        self.assertFalse(os.access(self.cache.filename, os.F_OK))
        self.assertRaises(OSError, self.cache.delete)
