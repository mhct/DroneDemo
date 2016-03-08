import sys
from PyQt4 import QtGui

from View import View
from gui.DrawingHelper import DrawingHelper
from gui.HttpDroneInterface import HttpDroneInterface
from gui.MapSetter import MapSetter
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse


class Controller:
    def __init__(self):
        # initialize the client
        self._drone_interface = HttpDroneInterface()

        # initialize the virtual object warehouse
        self._warehouse = VirtualObjectWarehouse("../virtualobjects", "virtual_object")

        # initialize the view
        self._map_params = self._drone_interface.get_map_params()
        self._view = View(self._map_params.map_width, self._map_params.resolution, self)

        # subscribe signal received from server
        self._drone_interface.drone_pose_update_signal.connect(self._update_drone_pose)
        self._drone_interface.virtual_env_update_signal.connect(self._update_virtual_env)

        # map setter, to update the map using the input from users
        self._map_setter = MapSetter(self._drone_interface, self._warehouse)

    def _update_drone_pose(self, drone_pose):
        drone_mesh = DrawingHelper.create_drone_mesh(drone_pose, self._map_params.resolution)
        self._view.draw_new_drone_pose(drone_mesh)

    def _update_virtual_env(self, elevation_map, object_hashcodes):
        elevation_map_mesh = DrawingHelper.create_elevation_map_mesh(elevation_map, self._map_params.resolution)
        self._view.draw_new_elevation_map(elevation_map_mesh)
        self._view.update_added_object_list(object_hashcodes)

    def set_map(self, file_names):
        self._map_setter.set_map(file_names)

    def get_existing_object_hashcodes(self):
        return self._drone_interface.get_existing_object_hashcodes()

    def get_drone_pose(self):
        return self._drone_interface.get_drone_pose()

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
