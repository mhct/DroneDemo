from PyQt4.QtCore import QThread

from Helper import MapWidth, Resolution, Point
from VirtualEnvironment import VirtualEnvironment
from PyQt4 import QtCore
from random import randint


class MockServer(QtCore.QThread):
    def __init__(self):
        QThread.__init__(self)
        self._env = VirtualEnvironment(MapWidth(50, 50), Resolution(100, 100))
        self._observers = []
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
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_drone_pose(self):
        for observer in self._observers:
                observer.update_drone_pose(self._drone_pose)

    def _notify_changed_environment(self):
        for observer in self._observers:
            observer.update_virtual_environment(self._env.get_elevation_map(), self.get_existing_object_hashcodes())

    def get_elevation_map(self):
        return self._env.get_elevation_map()

    def update_virtual_environment(self, to_be_added_objects, to_be_removed_object_hashcodes):
        added_object_hashcodes = []

        for virtual_object in to_be_added_objects:
            added_object_hashcodes.append(self.add_virtual_object(virtual_object))

        for hashcode in to_be_removed_object_hashcodes:
            self.remove_virtual_object(hashcode)

        self._notify_changed_environment()

        return added_object_hashcodes

    def add_virtual_object(self, virtual_object):
        return self._env.add_virtual_object(virtual_object)

    def remove_virtual_object(self, virtual_object_hashcode):
        self._env.remove_virtual_object_by_hashcode(virtual_object_hashcode)

    def get_map_params(self):
        return self._env.get_map_params()

    def get_existing_object_hashcodes(self):
        return self._env.get_all_object_hashcodes()

    def get_drone_pose(self):
        return Point(0, 0, 0)
