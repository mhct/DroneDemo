import numpy as np
from PyQt4 import QtCore
from DrawingHelper import DrawingHelper

from HttpDroneInterface import HttpDroneInterface
from Helper import Point, Mesh


class MapGetter(QtCore.QThread):
    map_signal = QtCore.pyqtSignal(object, object)

    def __init__(self, drone_interface):
        """
        :param drone_interface: the http client instance
        :type drone_interface: HttpDroneInterface
        :return:
        :rtype:
        """
        QtCore.QThread.__init__(self)
        self._drone_interface = drone_interface

    def run(self):
        """
        Update map for each one second
        """
        while True:
            elevation_map = self._drone_interface.get_elevation_map()
            drone_position = self._drone_interface.get_drone_position()
            mesh = self._generate_mesh(elevation_map, drone_position)
            object_hashcodes = self._drone_interface.get_existing_object_hashcodes()
            self.map_signal.emit(mesh, object_hashcodes)
            self.sleep(1)

    def _generate_mesh(self, elevation_map, drone_position):
        """
        Draw the elevation map
        :param elevation_map: the given elevation map
        :type elevation_map: 2D list
        :param drone_position: the current position of the drone
        :type Point
        """
        res = self._drone_interface.get_map_params().resolution
        object_mesh = DrawingHelper.create_elevation_map_mesh(elevation_map, res)
        drone_mesh = DrawingHelper.create_drone_mesh(drone_position, res)

        return Mesh(object_mesh, drone_mesh)
