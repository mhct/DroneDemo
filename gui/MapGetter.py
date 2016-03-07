import numpy as np
from PyQt4 import QtCore
from DrawingHelper import DrawingHelper

from HttpDroneInterface import HttpDroneInterface
from Helper import Point, Mesh


class MapGetter(QtCore.QThread):
    map_signal = QtCore.pyqtSignal(object, object)

    def __init__(self, http_client):
        """
        :param http_client: the http client instance
        :type http_client: HttpDroneInterface
        :return:
        :rtype:
        """
        QtCore.QThread.__init__(self)
        self._http_client = http_client

    def run(self):
        """
        Update map for each one second
        """
        while True:
            elevation_map = self._http_client.get_map()
            drone_position = self._http_client.get_drone_position()
            mesh = self._generate_mesh(elevation_map, drone_position)
            object_ids = self._http_client.get_existing_object_ids()
            self.map_signal.emit(mesh, object_ids)
            self.sleep(1)

    def _generate_mesh(self, elevation_map, drone_position):
        """
        Draw the elevation map
        :param elevation_map: the given elevation map
        :type elevation_map: 2D list
        :param drone_position: the current position of the drone
        :type Point
        """
        res = self._http_client.get_resolution()
        object_mesh = DrawingHelper.create_elevation_map_mesh(elevation_map, res)
        drone_mesh = DrawingHelper.create_drone_mesh(drone_position, res)
        return Mesh(object_mesh, drone_mesh)
