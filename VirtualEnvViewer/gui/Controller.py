from PyQt4 import QtCore
from PyQt4.QtCore import QObject

from VirtualEnvViewer.gui.MapSetter import MapSetter
from VirtualEnvViewer.gui.VirtualEnvironmentGetter import VirtualEnvironmentGetter


class Controller(QObject):

    drone_pose_update_signal = QtCore.pyqtSignal()
    virtual_env_update_signal = QtCore.pyqtSignal()

    def __init__(self, drone_connector, virtual_environment_service, warehouse):
        # initialize the client
        QObject.__init__(self)
        self._virtual_environment_service = virtual_environment_service

        # initialize the virtual object warehouse
        self._warehouse = warehouse

        # during the initialization, update the env_configuration and virtual_objects once
        (env_configuration, virtual_objects) = self._virtual_environment_service.get_elevation_map()
        self._warehouse.replace_virtual_environment_objects(virtual_objects)

        self._env_configuration = env_configuration

        self._drone_pose = None
        self._drone_connector = drone_connector

        # subscribe signal received from server
        self._drone_connector.drone_pose_update_signal.connect(self._update_drone_pose)

        # map setter, to update the map using the input from users
        self._map_setter = MapSetter(self._virtual_environment_service)

        # thread to update virtual environment after each second
        self._virtual_environment_getter = VirtualEnvironmentGetter(self._virtual_environment_service)
        self._virtual_environment_getter.map_signal.connect(self._update_virtual_env)
        self._virtual_environment_getter.start()

    def get_map_params(self):
        return self._env_configuration

    def _update_drone_pose(self, drone_pose):
        self._drone_pose = drone_pose
        self.drone_pose_update_signal.emit()

    def _update_virtual_env(self, env_configuration, virtual_objects):
        self._env_configuration = env_configuration
        self._warehouse.replace_virtual_environment_objects(virtual_objects)
        self.virtual_env_update_signal.emit()

    def set_map(self, virtual_objects):
        self._map_setter.set_map(virtual_objects, self._warehouse.get_virtual_environment_objects())

    def get_added_objects(self):
        return self._warehouse.get_virtual_environment_objects()

    def get_drone_pose(self):
        return self._drone_pose

    def get_elevation_map(self):
        return self._elevation_map

    def get_all_objects_in_warehouse(self):
        return self._warehouse.get_all_objects()
