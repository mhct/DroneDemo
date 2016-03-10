from PyQt4 import QtCore

from PyQt4.QtCore import QObject

from VirtualEnvViewer.gui import MapSetter


class Controller(QObject):

    drone_pose_update_signal = QtCore.pyqtSignal()
    virtual_env_update_signal = QtCore.pyqtSignal()

    def __init__(self, drone_interface, warehouse):
        # initialize the client
        QObject.__init__(self)
        self._drone_interface = drone_interface

        # initialize the virtual object warehouse
        self._warehouse = warehouse
        self._warehouse.update_added_objects(self._drone_interface.get_existing_objects())

        self._drone_pose = self._drone_interface.get_drone_pose()
        self._elevation_map = self._drone_interface.get_elevation_map()

        # subscribe signal received from server
        self._drone_interface.drone_pose_update_signal.connect(self._update_drone_pose)
        self._drone_interface.virtual_env_update_signal.connect(self._update_virtual_env)

        # map setter, to update the map using the input from users
        self._map_setter = MapSetter(self._drone_interface)

    def get_map_params(self):
        return self._drone_interface.get_map_params()

    def _update_drone_pose(self, drone_pose):
        self._drone_pose = drone_pose
        self.drone_pose_update_signal.emit()

    def _update_virtual_env(self, elevation_map, virtual_objects):
        self._elevation_map = elevation_map
        self._warehouse.update_added_objects(virtual_objects)
        self.virtual_env_update_signal.emit()

    def set_map(self, virtual_objects):
        self._map_setter.set_map(virtual_objects, self._warehouse.get_added_objects())

    def get_added_objects(self):
        return self._warehouse.get_added_objects()

    def get_drone_pose(self):
        return self._drone_pose

    def get_elevation_map(self):
        return self._elevation_map

    def get_all_objects_in_warehouse(self):
        return self._warehouse.get_all_objects()
