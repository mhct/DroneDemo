import sys
from PyQt4 import QtGui

from View import View
from gui.HttpClient import HttpClient
from gui.MapGetter import MapGetter
from gui.MapSetter import MapSetter


class Controller:
    def __init__(self):
        # initialize the client
        self._http_client = HttpClient()
        # initialize the view
        self._view = View(self._http_client.get_map_width(), self._http_client.get_resolution(), self)
        # thread that constantly request map and drone position after each second
        self._map_getter = MapGetter(self._http_client)
        self._map_getter.map_signal.connect(self._update_drone_info)
        self._map_getter.start()
        # map setter, to update the map using the input from users
        self._map_setter = MapSetter(self._http_client)

    def _update_drone_info(self, mesh, object_ids):
        self._view.draw_objects_and_drone(mesh)
        self._view.update_list_object_ids(object_ids)

    def set_map(self, object_ids):
        self._map_setter.set_map(object_ids)

    def get_existing_object_ids(self):
        return self._http_client.get_existing_object_ids()

    def get_drone_state(self):
        return self._http_client.get_drone_position()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
