import sys
from PyQt4 import QtGui

from View import View
from gui.HttpDroneInterface import HttpDroneInterface
from gui.MapGetter import MapGetter
from gui.MapSetter import MapSetter
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse


class Controller:
    def __init__(self):
        # initialize the client
        self._drone_interface = HttpDroneInterface()

        # initialize the virtual object warehouse
        self._warehouse = VirtualObjectWarehouse("../virtualobjects", "virtual_object")

        # initialize the view
        map_params = self._drone_interface.get_map_params()
        self._view = View(map_params.map_width, map_params.resolution, self)

        # thread that constantly request map and drone position after each second
        self._map_getter = MapGetter(self._drone_interface)
        self._map_getter.map_signal.connect(self._update_drone_info)
        self._map_getter.start()

        # map setter, to update the map using the input from users
        self._map_setter = MapSetter(self._drone_interface, self._warehouse)

    def _update_drone_info(self, mesh, object_ids):
        self._view.draw_objects_and_drone(mesh)
        self._view.update_added_object_list(object_ids)

    def set_map(self, file_names):
        self._map_setter.set_map(file_names)

    def get_existing_object_ids(self):
        return self._drone_interface.get_existing_object_ids()

    def get_drone_state(self):
        return self._drone_interface.get_drone_position()

    def get_all_object_file_names(self):
        return self._warehouse.get_all_object_file_names()

    def get_file_name_by_hashcode(self, hashcode):
        return self._warehouse.get_file_name_by_hashcode(hashcode)

    def get_object_by_file_name(self, file_name):
        return self._warehouse.get_virtual_object_by_filename(file_name)

    def get_object_by_hashcode(self, hashcode):
        return self._warehouse.get_virtual_object_by_hashcode(hashcode)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
