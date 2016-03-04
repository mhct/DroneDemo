from Environment import Environment
from VirtualObject import VirtualObject


class HttpClient:
    def __init__(self):
        pass

    def get_map(self):
        env = Environment(4, 4, 1, 1)
        virtual_object = VirtualObject("../virtualobjects/test_gui.txt")
        env.add_virtual_object(virtual_object)
        return env.get_elevation_map()
