import os
import time
import unittest

import fcache


class testCache(unittest.TestCase):

    def setUp(self):
        self.cache = fcache.Cache("unittest", "fcache", "Thomas Roten")
        self.cache.set("num", 43)
        self.cache.set("timer", 1, 2)

    def tearDown(self):
        self.cache.delete()
        self.cache = None

    def test_init(self):
        self.assertTrue(os.access(self.cache.filename, os.F_OK))

    def test_get(self):
        self.assertEqual(self.cache.get("num"), 43)
        self.assertEqual(self.cache.get("alsdf"), None)
        self.assertEqual(self.cache.get("timer"), 1)
        time.sleep(2)
        self.assertEqual(self.cache.get("timer"), None)

    def test_remove(self):
        self.assertTrue(self.cache.remove("num"))
        self.assertEqual(self.cache.get("num"), None)
        self.assertFalse(self.cache.remove("jlk"))

    def test_delete(self):
        self.assertTrue(self.cache.delete())
        self.assertFalse(os.access(self.cache.filename, os.F_OK))
        self.assertFalse(self.cache.delete())
