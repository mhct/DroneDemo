import numpy as np
from PyQt4 import QtCore
from SurfaceConstructor import SurfaceConstructor

from HttpClient import HttpClient
import pyqtgraph.opengl as gl
from Helper import Point, Mesh


class MapGetter(QtCore.QThread):
    map_signal = QtCore.pyqtSignal(object, object)

    def __init__(self, http_client):
        """
        :param http_client: the http client instance
        :type http_client: HttpClient
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
        object_mesh = self._create_object_mesh(elevation_map, res)
        drone_mesh = self._create_drone_mesh(drone_position, res)
        return Mesh(object_mesh, drone_mesh)

    def _create_drone_mesh(self, drone_position, resolution):
        drone_shape = SurfaceConstructor.construct_drone(drone_position, resolution)
        drone_mesh = gl.GLMeshItem(vertexes=np.array(drone_shape), color=(1, 0, 0, 1), smooth=False, glOptions='opaque')
        return drone_mesh

    def _create_object_mesh(self, elevation_map, resolution):
        surfaces = []
        for x in range(len(elevation_map)):
            for y in range(len(elevation_map[0])):
                if elevation_map[x][y] > 0:
                    cube = SurfaceConstructor.construct_cube(x * resolution.x, y * resolution.y, resolution,
                                                             elevation_map[x][y])
                    surfaces += cube

        if len(surfaces) == 0:
            object_mesh = None
        else:
            object_mesh = gl.GLMeshItem(vertexes=np.array(surfaces), color=(0, 0, 1, 1), smooth=False, shader='shaded',
                                        glOptions='opaque')

        return object_mesh
