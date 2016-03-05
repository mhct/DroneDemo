import numpy as np
from PyQt4 import QtCore
from HttpClient import HttpClient
import pyqtgraph.opengl as gl


class MapGetter(QtCore.QThread):
    map_signal = QtCore.pyqtSignal(object)

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
            mesh = self._generate_mesh(elevation_map)
            self.map_signal.emit(mesh)
            self.sleep(1)

    def _generate_mesh(self, elevation_map):
        """
        Draw the elevation map
        :param elevation_map: the given elevation map
        :type elevation_map: 2D list
        """
        res = self._http_client.get_resolution()
        all_cubes = []
        for x in range(len(elevation_map)):
            for y in range(len(elevation_map[0])):
                if elevation_map[x][y] > 0:
                    cube = self._construct_cube(x * res.x, y * res.y, res.x, res.y, elevation_map[x][y])
                    all_cubes += cube

        if len(all_cubes) == 0:
            return None

        mesh = gl.GLMeshItem(vertexes=np.array(all_cubes), color=(0, 0, 1, 1), smooth=False, shader='shaded',
                             glOptions='opaque')

        return mesh

    def _construct_cube(self, pos_x, pos_y, res_x, res_y, height):
        """
        Construct the cube given its origin corner (the one with the smallest x and y values), the resolution of each
        cell and the height
        :param pos_x: x coordinate
        :type pos_x: int
        :param pos_y: y coordinate
        :type pos_y: int
        :param res_x: resolution in x coordinate (millimeters)
        :type res_x: int
        :param res_y: resolution in y coordinate (millimeters)
        :type res_y: int
        :param height: the height of the cube
        :type height: int (millimeters)
        :return: the cube as a list of triangular surface in mesh format that pyqtgraph can understand
        :rtype: array
        """

        p0 = [pos_x, pos_y, 0]
        p1 = [pos_x + res_x, pos_y, 0]
        p2 = [pos_x + res_x, pos_y + res_y, 0]
        p3 = [pos_x, pos_y + res_y, 0]
        p4 = [pos_x, pos_y, height]
        p5 = [pos_x + res_x, pos_y, height]
        p6 = [pos_x + res_x, pos_y + res_y, height]
        p7 = [pos_x, pos_y + res_y, height]

        constructed_cube = [[p0, p1, p2], [p0, p2, p3], [p4, p5, p6], [p4, p6, p7], [p0, p1, p5], [p0, p5, p4],
                            [p1, p2, p6], [p1, p6, p5], [p2, p3, p7], [p2, p7, p6], [p0, p3, p7], [p0, p7, p4]]

        return constructed_cube
