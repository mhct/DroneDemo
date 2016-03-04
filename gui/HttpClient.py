from Environment import Environment
from VirtualObject import VirtualObject


class HttpClient:
    def __init__(self):
        self._env = Environment(50, 50, 100, 100)

    def get_map(self):
        return self._env.get_elevation_map()

    def add_virtual_object(self, file_name):
        virtual_object = VirtualObject("../virtualobjects/" + file_name)
        self._env.add_virtual_object(virtual_object)

    def get_resolution(self):
        return self._env.get_resolution()
