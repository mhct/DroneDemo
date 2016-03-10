from PyQt4 import QtCore
from random import randint

from PyQt4.QtCore import QThread

from VirtualEnvViewer.Helper import MapWidth, Resolution, Point
from Server import VirtualEnvironment


class MockServer(QtCore.QThread):
    def __init__(self):
        QThread.__init__(self)
        self._env = VirtualEnvironment(MapWidth(50, 50), Resolution(100, 100))
        self._observers = set()
        self._drone_pose = Point(0, 0, 0)

    def run(self):
        """
        Update drone pose for each 100 milliseconds
        """
        while True:
            self._drone_pose = Point(randint(0, 5000), randint(0, 5000), randint(0, 5000))
            self._notify_drone_pose()
            self.msleep(1000)

    def register(self, observer):
        self._observers.add(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def _notify_drone_pose(self):
        for observer in self._observers:
            observer.update_drone_pose(self._drone_pose)

    def _notify_changed_environment(self):
        for observer in self._observers:
            observer.update_virtual_environment(self.get_elevation_map(), self.get_existing_virtual_objects())

    def get_elevation_map(self):
        return self._env.get_elevation_map()

    def get_existing_virtual_objects(self):
        return self._env.get_virtual_objects()

    def update_virtual_environment(self, to_be_added_objects, to_be_removed_objects):
        for virtual_object in to_be_added_objects:
            self._env.add_virtual_object(virtual_object)

        for virtual_object in to_be_removed_objects:
            self._env.remove_virtual_object(virtual_object)

        self._notify_changed_environment()

    def get_map_params(self):
        return self._env.get_map_params()

    def get_drone_pose(self):
        return Point(0, 0, 0)
