import unittest

from VirtualObject import VirtualObject
from VirtualEnvironment import VirtualEnvironment
from Helper import Point, MapWidth, Resolution
from MD5Generator import md5


class VirtualEnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.env = VirtualEnvironment(MapWidth(4, 4), Resolution(100, 100))  # size_x size_y res_x res_y
        self._virtual_object1 = VirtualObject("virtualobjects/test_object1.txt")
        self._virtual_object2 = VirtualObject("virtualobjects/test_object2.txt")

    def test_correct_input_test_files(self):
        self.assertEqual(md5("virtualobjects/test_object1.txt"), "914487f5ff43a13a5929dc31afb9b541")
        self.assertEqual(md5("virtualobjects/test_object2.txt"), "f2b109928cc97dc43ed9b633e8d20883")

    def test_add_object(self):
        self.env.add_virtual_object(self._virtual_object1)

        self.assertTrue(self.env.is_occupied(Point(150, 150, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_occupied(Point(150, 250, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_occupied(Point(150, 350, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 350, 1001)))

        self.assertFalse(self.env.is_occupied(Point(50, 150, 1)))

    def test_add_two_objects(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)

        self.assertTrue(self.env.is_occupied(Point(150, 50, 1999)))
        self.assertFalse(self.env.is_occupied(Point(150, 50, 2001)))

        self.assertTrue(self.env.is_occupied(Point(150, 150, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_occupied(Point(150, 250, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_occupied(Point(150, 350, 1999)))
        self.assertFalse(self.env.is_occupied(Point(150, 350, 2001)))

    def test_remove_object_case1(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.remove_virtual_object(self._virtual_object1)

        self.assertFalse(self.env.is_occupied(Point(150, 150, 500)))
        self.assertFalse(self.env.is_occupied(Point(150, 250, 500)))
        self.assertFalse(self.env.is_occupied(Point(150, 350, 500)))
        self.assertFalse(self.env.is_occupied(Point(50, 150, 500)))

    def test_remove_object_case2(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)
        self.env.remove_virtual_object(self._virtual_object2)

        self.assertTrue(self.env.is_occupied(Point(150, 150, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_occupied(Point(150, 250, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_occupied(Point(150, 350, 999)))
        self.assertFalse(self.env.is_occupied(Point(150, 350, 1001)))

        self.assertFalse(self.env.is_occupied(Point(50, 150, 1)))

    def test_clear_map(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.clear_map()
        self.assertFalse(self.env.is_occupied(Point(150, 150, 999)))

    def test_get_all_object_ids(self):
        self.assertEqual(self.env.get_all_object_hashcodes(), [])

        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)

        self.assertEqual(self.env.get_all_object_hashcodes(), [hash(self._virtual_object1), hash(self._virtual_object2)])

        self.env.remove_virtual_object(self._virtual_object1)
        self.assertEqual(self.env.get_all_object_hashcodes(), [hash(self._virtual_object2)])

if __name__ == '__main__':
    unittest.main()
