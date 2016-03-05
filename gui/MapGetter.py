import numpy as np
from PyQt4 import QtCore
from HttpClient import HttpClient
import pyqtgraph.opengl as gl
from Helper import Point, Mesh


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
            drone_position = self._http_client.get_drone_position()
            mesh = self._generate_mesh(elevation_map, drone_position)
            self.map_signal.emit(mesh)
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

        # TODO rename
        all_cubes = []
        # draw virtual objects
        for x in range(len(elevation_map)):
            for y in range(len(elevation_map[0])):
                if elevation_map[x][y] > 0:
                    cube = self._construct_cube(x * res.x, y * res.y, res.x, res.y, elevation_map[x][y])
                    all_cubes += cube

        if len(all_cubes) == 0:
            object_mesh = None
        else:
            object_mesh = gl.GLMeshItem(vertexes=np.array(all_cubes), color=(0, 0, 1, 1), smooth=False, shader='shaded',
                                        glOptions='opaque')

        # draw the drone
        drone_shape = self._construct_drone_shape(drone_position, res.x, res.y)
        drone_mesh = gl.GLMeshItem(vertexes=np.array(drone_shape), color=(1, 0, 0, 1), smooth=False, glOptions='opaque')

        return Mesh(object_mesh, drone_mesh)

    def _construct_drone_shape(self, drone_position, res_x, res_y):
        # TODO add direction

        p0 = [drone_position.x + res_x / 2, drone_position.y + res_y / 2, drone_position.z]
        p1 = [drone_position.x - res_x / 2, drone_position.y + res_y / 2, drone_position.z]
        p2 = [drone_position.x - res_x / 2, drone_position.y - res_y / 2, drone_position.z]
        p3 = [drone_position.x + res_x / 2, drone_position.y - res_y / 2, drone_position.z]

        drone_shape = [[p0, p1, p2], [p0, p3, p2]]

        return drone_shape

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
