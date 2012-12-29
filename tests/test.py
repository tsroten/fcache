import os
import unittest

import fcache.fcache


class testCache(unittest.TestCase):

    def setUp(self):
        self.cache = fcache.fcache.Cache("unittest", "fcache", "Thomas Roten")
        self.cache.set("num", 43)

    def tearDown(self):
        self.cache.delete()

    def test_init(self):
        self.assertTrue(os.access(self.cache.filename, os.F_OK))

    def test_get(self):
        self.assertEqual(self.cache.get("num"), 43)

    def test_remove(self):
        self.cache.remove("num")
        self.assertEqual(self.cache.get("num"), None)

    def test_delete(self):
        self.cache.delete()
        self.assertFalse(os.access(self.cache.filename, os.F_OK))
