import unittest

from mock import patch

from VirtualObject import VirtualObject
from VirtualEnvViewer.gui import MapSetter
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse


class MyTestCase(unittest.TestCase):
    def setUp(self):
        patcher = patch('gui.HttpDroneInterface.HttpDroneInterface')
        mock_http_client = patcher.start()
        warehouse = VirtualObjectWarehouse("../resources_virtualobjects", "virtual_object")
        self._map_setter = MapSetter(mock_http_client, warehouse)
        self.virtual_object1 = VirtualObject("../resources_virtualobjects/virtual_object1.txt")
        self.virtual_object2 = VirtualObject("../resources_virtualobjects/virtual_object2.txt")
        self.virtual_object3 = VirtualObject("../resources_virtualobjects/virtual_object3.txt")

    def test_get_to_be_removed_objects(self):
        new_objects = [self.virtual_object3]
        existing_objects = [self.virtual_object1, self.virtual_object3]
        self.assertListEqual(self._map_setter._get_to_be_removed_objects(existing_objects, new_objects),
                             [self.virtual_object1])

if __name__ == '__main__':
    unittest.main()
