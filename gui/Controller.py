import sys
from PyQt4 import QtGui

from View import View
from gui.HttpClient import HttpClient
from gui.MapGetter import MapGetter
from gui.MapSetter import MapSetter


class Controller:
    def __init__(self):
        # keep a reference to threads, to keep them alive
        self._threads = []
        # initialize the client
        self._http_client = HttpClient()
        # initialize the view
        self._view = View(self._http_client.get_map_width(), self._http_client.get_resolution(), self)
        # thread that constantly request map and drone position after each second
        self._map_getter = MapGetter(self._http_client)
        self._map_getter.map_signal.connect(self._update_3d_view)
        self._map_getter.start()
        # map setter, to update the map using the input from users
        self._map_setter = MapSetter(self._http_client)

    def _update_3d_view(self, mesh):
        self._view.draw_3d_map(mesh)

    def set_map(self):
        checked_boxes = self._view.get_checked_boxes()

        object_ids = []
        for checkbox in checked_boxes:
            object_ids.append(int(checkbox.text()[-1]))

        self._map_setter.set_map(object_ids)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
