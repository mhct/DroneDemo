import unittest

from mock import Mock, patch

from VirtualObject import VirtualObject
from gui.MapSetter import MapSetter


class MyTestCase(unittest.TestCase):
    def setUp(self):
        patcher = patch('gui.HttpDroneInterface.HttpDroneInterface')
        mock_http_client = patcher.start()
        self._map_setter = MapSetter(mock_http_client)
        self.virtual_object1 = VirtualObject("../virtualobjects/main_object1.txt")
        self.virtual_object2 = VirtualObject("../virtualobjects/main_object2.txt")
        self.virtual_object3 = VirtualObject("../virtualobjects/main_object3.txt")

    def test_get_to_be_removed_objects(self):
        new_objects = [3]
        existing_objects = [1, 3]
        self.assertListEqual(self._map_setter._get_to_be_removed_objects(existing_objects, new_objects),
                             [self.virtual_object1])

if __name__ == '__main__':
    unittest.main()
