import unittest

from VirtualObject import VirtualObject
from Environment import Environment
from Helper import Point
from MD5Generator import md5


class EnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.env = Environment(4, 4, 100, 100)  # size_x size_y res_x res_y

    def test_correct_input_test_files(self):
        self.assertEqual(md5("virtualobjects/test_object1.txt"), "7a3fcfcb6ff9eee335a334ce454dd02e")
        self.assertEqual(md5("virtualobjects/test_object2.txt"), "eb5487ad0d4fb91e894ab9fbf631333c")

    def test_add_object(self):
        virtual_object = VirtualObject("virtualobjects/test_object1.txt")
        self.env.add_virtual_object(virtual_object)

        self.assertTrue(self.env.is_in_object_region(Point(150, 150, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 250, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 350, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 350, 1001)))

        self.assertFalse(self.env.is_in_object_region(Point(50, 150, 1)))

    def test_add_two_objects(self):
        virtual_object1 = VirtualObject("virtualobjects/test_object1.txt")
        virtual_object2 = VirtualObject("virtualobjects/test_object2.txt")
        self.env.add_virtual_object(virtual_object1)
        self.env.add_virtual_object(virtual_object2)

        self.assertTrue(self.env.is_in_object_region(Point(150, 50, 1999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 50, 2001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 150, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 250, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 350, 1999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 350, 2001)))

    def test_remove_object_case1(self):
        virtual_object = VirtualObject("virtualobjects/test_object1.txt")
        self.env.add_virtual_object(virtual_object)
        self.env.remove_virtual_object(virtual_object)

        self.assertFalse(self.env.is_in_object_region(Point(150, 150, 500)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 250, 500)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 350, 500)))
        self.assertFalse(self.env.is_in_object_region(Point(50, 150, 500)))

    def test_remove_object_case2(self):
        virtual_object1 = VirtualObject("virtualobjects/test_object1.txt")
        virtual_object2 = VirtualObject("virtualobjects/test_object2.txt")
        self.env.add_virtual_object(virtual_object1)
        self.env.add_virtual_object(virtual_object2)
        self.env.remove_virtual_object(virtual_object2)

        self.assertTrue(self.env.is_in_object_region(Point(150, 150, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 150, 1001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 250, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 250, 1001)))

        self.assertTrue(self.env.is_in_object_region(Point(150, 350, 999)))
        self.assertFalse(self.env.is_in_object_region(Point(150, 350, 1001)))

        self.assertFalse(self.env.is_in_object_region(Point(50, 150, 1)))

    def test_clear_map(self):
        virtual_object = VirtualObject("virtualobjects/test_object1.txt")
        self.env.add_virtual_object(virtual_object)
        self.env.clear_map()
        self.assertFalse(self.env.is_in_object_region(Point(150, 150, 999)))

    def test_get_all_object_ids(self):
        self.assertEqual(self.env.get_all_object_ids(), [])

        virtual_object1 = VirtualObject("virtualobjects/test_object1.txt")
        virtual_object2 = VirtualObject("virtualobjects/test_object2.txt")
        self.env.add_virtual_object(virtual_object1)
        self.env.add_virtual_object(virtual_object2)

        self.assertEqual(self.env.get_all_object_ids(), [1, 2])

        self.env.remove_virtual_object(virtual_object1)
        self.assertEqual(self.env.get_all_object_ids(), [2])

if __name__ == '__main__':
    unittest.main()
