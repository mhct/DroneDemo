import unittest

from VirtualObject import VirtualObject
from VirtualObjectWarehouse import VirtualObjectWarehouse


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._warehouse = VirtualObjectWarehouse("../virtualobjects", "test_object")
        self._object1 = VirtualObject("../virtualobjects/test_object1.txt")
        self._object2 = VirtualObject("../virtualobjects/test_object2.txt")

    def test_get_object_by_file_name(self):
        self.assertEqual(self._warehouse.get_virtual_object_by_filename("test_object1.txt"), self._object1)
        self.assertEqual(self._warehouse.get_virtual_object_by_filename("test_object2.txt"), self._object2)

    def test_update_hashcode(self):
        self._warehouse.update_virtual_object_hashcode("test_object1.txt", hash(self._object1))
        self._warehouse.update_virtual_object_hashcode("test_object2.txt", hash(self._object2))

        self.assertEqual(self._warehouse.get_virtual_object_by_hashcode(hash(self._object1)), self._object1)
        self.assertEqual(self._warehouse.get_virtual_object_by_hashcode(hash(self._object2)), self._object2)


if __name__ == '__main__':
    unittest.main()
