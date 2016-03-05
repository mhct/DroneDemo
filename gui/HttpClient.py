from Environment import Environment
from Helper import Point


class HttpClient:
    def __init__(self):
        self._env = Environment(50, 50, 100, 100)

    def get_map(self):
        return self._env.get_elevation_map()

    def add_virtual_object(self, virtual_object):
        self._env.add_virtual_object(virtual_object)

    def get_map_width(self):
        return self._env.get_map_width()

    def get_resolution(self):
        return self._env.get_resolution()

    def get_existing_object_ids(self):
        return self._env.get_all_object_ids()

    def remove_virtual_object(self, virtual_object):
        self._env.remove_virtual_object(virtual_object)

    def get_drone_position(self):
        return Point(0, 0, 0)