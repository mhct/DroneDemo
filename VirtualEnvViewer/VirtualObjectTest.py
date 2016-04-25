import unittest

from MD5Generator import md5
from VirtualObject import VirtualObject


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._object1 = VirtualObject("resources_virtualobjects/test_object1.txt")
        self._object2 = VirtualObject("resources_virtualobjects/test_object2.txt")
        self._another_object1 = VirtualObject("resources_virtualobjects/test_object1.txt")

    def test_correct_input_files(self):
        self.assertEqual(md5("resources_virtualobjects/test_object1.txt"), "914487f5ff43a13a5929dc31afb9b541")
        self.assertEqual(md5("resources_virtualobjects/test_object2.txt"), "f2b109928cc97dc43ed9b633e8d20883")

    def test_equality(self):
        self.assertEqual(self._object1, self._another_object1)
        self.assertNotEqual(self._object1, self._object2)

    def test_hash(self):
        self.assertEqual(hash(self._object1), hash(self._another_object1))
        self.assertNotEqual(hash(self._object1), hash(self._object2))

if __name__ == '__main__':
    unittest.main()
