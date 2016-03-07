from Environment import Environment
from Helper import Point, MapWidth, Resolution


class HttpDroneInterface:
    def __init__(self):
        self._env = Environment(MapWidth(50, 50), Resolution(100, 100))

    def get_elevation_map(self):
        return self._env.get_elevation_map()

    def add_virtual_object(self, virtual_object):
        return self._env.add_virtual_object(virtual_object)

    def remove_virtual_object(self, virtual_object_hashcode):
        self._env.remove_virtual_object_by_hashcode(virtual_object_hashcode)

    def get_map_params(self):
        return self._env.get_map_params()

    def get_existing_object_hashcodes(self):
        return self._env.get_all_object_hashcodes()

    def get_drone_position(self):
        return Point(0, 0, 0)