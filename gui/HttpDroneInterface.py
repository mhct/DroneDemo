from abc import ABCMeta

from PyQt4 import QtCore
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtWrapperType

from Helper import MapWidth, Resolution
from VirtualEnvironment import VirtualEnvironment
from gui.DroneObserver import DroneObserver
from gui.MockServer import MockServer


class FinalMeta(ABCMeta, pyqtWrapperType):
    pass


class HttpDroneInterface(DroneObserver, QObject):
    __metaclass__ = FinalMeta

    drone_pose_update_signal = QtCore.pyqtSignal(object)
    virtual_env_update_signal = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super(HttpDroneInterface, self).__init__()
        self._env = VirtualEnvironment(MapWidth(50, 50), Resolution(100, 100))
        self._server = None
        self.subcribe_server()

    def subcribe_server(self):
        self._server = MockServer()
        self._server.start()
        self._server.register(self)

    def get_elevation_map(self):
        return self._server.get_elevation_map()

    def send_update_command(self, to_be_added_objects, to_be_removed_objects):
        return self._server.update_virtual_environment(to_be_added_objects, to_be_removed_objects)

    def get_map_params(self):
        return self._server.get_map_params()

    def get_existing_objects(self):
        return self._server.get_existing_virtual_objects()

    def get_drone_pose(self):
        return self._server.get_drone_pose()

    def update_drone_pose(self, drone_pose):
        self.drone_pose_update_signal.emit(drone_pose)

    def update_virtual_environment(self, elevation_map, existing_objects):
        self.virtual_env_update_signal.emit(elevation_map, existing_objects)
