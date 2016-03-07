import unittest

from CellData import CellData
from MD5Generator import md5
from VirtualObject import VirtualObject


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._cell_data = CellData()
        self._object1 = VirtualObject("virtualobjects/test_object1.txt")
        self._object2 = VirtualObject("virtualobjects/test_object2.txt")

    def test_correct_input_files(self):
        self.assertEqual(md5("virtualobjects/test_object1.txt"), "914487f5ff43a13a5929dc31afb9b541")
        self.assertEqual(md5("virtualobjects/test_object2.txt"), "f2b109928cc97dc43ed9b633e8d20883")

    def test_add_object(self):
        # initially, no object exists
        self.assertFalse(self._cell_data.is_occupied(1))

        self._cell_data.add_virtual_object(self._object1, 10)
        self.assertTrue(self._cell_data.is_occupied(9))
        self.assertFalse(self._cell_data.is_occupied(11))

        self._cell_data.add_virtual_object(self._object2, 20)
        self.assertTrue(self._cell_data.is_occupied(19))
        self.assertFalse(self._cell_data.is_occupied(21))

    def test_remove_object(self):
        self._cell_data.add_virtual_object(self._object1, 10)
        self._cell_data.add_virtual_object(self._object2, 20)

        self._cell_data.remove_virtual_object(self._object2)
        self.assertTrue(self._cell_data.is_occupied(9))
        self.assertFalse(self._cell_data.is_occupied(11))

        self._cell_data.remove_virtual_object(self._object1)
        self.assertFalse(self._cell_data.is_occupied(1))

    def test_add_object_fail(self):
        self._cell_data.add_virtual_object(self._object1, 10)
        with self.assertRaises(ValueError):
            self._cell_data.add_virtual_object(self._object1, 10)

    def test_clear_cell(self):
        self._cell_data.add_virtual_object(self._object1, 10)
        self._cell_data.add_virtual_object(self._object2, 20)
        self._cell_data.clear_cell()

        self.assertFalse(self._cell_data.is_occupied(1))


if __name__ == '__main__':
    unittest.main()
