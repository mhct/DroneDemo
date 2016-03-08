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

    def add_virtual_object(self, virtual_object):
        return self._server.add_virtual_object(virtual_object)

    def remove_virtual_object(self, virtual_object_hashcode):
        self._server.remove_virtual_object(virtual_object_hashcode)

    def send_update_command(self, to_be_added_objects, to_be_removed_object_hashcodes):
        return self._server.update_virtual_environment(to_be_added_objects, to_be_removed_object_hashcodes)

    def get_map_params(self):
        return self._server.get_map_params()

    def get_existing_object_hashcodes(self):
        return self._server.get_existing_object_hashcodes()

    def get_drone_pose(self):
        return self._server.get_drone_pose()

    def update_drone_pose(self, drone_pose):
        self.drone_pose_update_signal.emit(drone_pose)

    def update_virtual_environment(self, elevation_map, object_hashcodes):
        self.virtual_env_update_signal.emit(elevation_map, object_hashcodes)
