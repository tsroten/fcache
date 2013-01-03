import datetime
import os
import time
import unittest

import fcache


class testCache(unittest.TestCase):

    def setUp(self):
        self.cache = fcache.Cache("unittest", "fcache")
        self.cache.set("n", 43)
        self.cache.set("p", 2)
        self.cache.set("timer", 1, 0.1)

    def tearDown(self):
        if os.access(self.cache.filename, os.F_OK) is True:
            self.cache.delete()
        self.cache = None

    def test_init(self):
        self.assertTrue(os.access(self.cache.filename, os.F_OK))

    def test_set(self):
        self.cache.delete()
        self.assertRaises(IOError, self.cache.set, "n", 43)

    def test_set_default(self):
        self.assertEqual(self.cache.set_default("n"), 43)
        self.assertEqual(self.cache.set_default("y", 2, .1), 2)
        self.assertEqual(self.cache.get("y"), 2)
        time.sleep(0.1)
        self.assertEqual(self.cache.get("y"), None)

    def test_get(self):
        self.assertEqual(self.cache.get("n"), 43)
        self.assertEqual(self.cache.get("timer"), 1)
        time.sleep(0.1)
        self.assertEqual(self.cache.get("timer"), None)
        self.assertEqual(self.cache.get("timer", True), 1)
        self.assertRaises(KeyError, self.cache.get, "j")
        self.cache.delete()
        self.assertRaises(IOError, self.cache.get, "j")

    def test_keys(self):
        self.assertEqual(sorted(self.cache.keys()), ["n", "p", "timer"])
        time.sleep(0.1)
        self.assertEqual(sorted(self.cache.keys()), ["n", "p"])
        self.assertEqual(sorted(self.cache.keys(True)), ["n", "p", "timer"])

    def test_values(self):
        self.assertEqual(sorted(self.cache.values()), [1, 2, 43])
        time.sleep(0.1)
        self.assertEqual(sorted(self.cache.values()), [2, 43])
        self.assertEqual(sorted(self.cache.values(True)), [1, 2, 43])

    def test_items(self):
        items = sorted(self.cache.items(), key=lambda data: data[0])
        self.assertEqual(items, [("n", 43), ("p", 2), ("timer", 1)])
        time.sleep(0.1)
        items = sorted(self.cache.items(), key=lambda data: data[0])
        self.assertEqual(items, [("n", 43), ("p", 2)])
        items = sorted(self.cache.items(True), key=lambda data: data[0])
        self.assertEqual(items, [("n", 43), ("p", 2), ("timer", 1)])

    def test_invalidate(self):
        self.assertEqual(self.cache.get("n"), 43)
        self.cache.invalidate("n")
        self.assertEqual(self.cache.get("n"), None)
        self.assertEqual(self.cache.get("p"), 2)
        self.cache.invalidate()
        self.assertEqual(self.cache.get("p"), None)
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


class testHelpers(unittest.TestCase):

    def setUp(self):
        self.cache = fcache.Cache("unittest", "fcache")

    def tearDown(self):
        self.cache.delete()

    def test_is_expired(self):
        now = datetime.datetime.now()
        j = {"expires": now, "data": None}
        k = {"expires": now + datetime.timedelta(seconds=10), "data": None}
        self.assertTrue(self.cache._is_expired(j))
        self.assertFalse(self.cache._is_expired(k))
