import numpy as np
from PyQt4 import QtGui
import pyqtgraph.opengl as gl

from HttpClient import HttpClient


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_widget = QtGui.QListWidget()
        self.button = QtGui.QPushButton("Start")
        self.button.clicked.connect(self._start_http_client)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        # layout.addWidget(self.list_widget)

        #######
        self.map_3d = gl.GLViewWidget()
        self.map_3d.show()
        self.map_3d.setWindowTitle('pyqtgraph example: GLMeshItem')
        self.map_3d.setCameraPosition(distance=40)

        g = gl.GLGridItem()
        g.scale(1, 1, 1)
        self.map_3d.addItem(g)

        cube = self._construct_cube(0, 0, 1, 1, 20)
        colors = np.tile([0, 0, 1, 0.7], (cube.size, 1))

        m1 = gl.GLMeshItem(vertexes=cube, faceColors=colors, smooth=False, shader='shaded', glOptions='opaque')
        m1.translate(5, 5, 0)
        m1.setGLOptions('additive')
        self.map_3d.addItem(m1)

        layout.addWidget(self.map_3d)
        #######

        self.setLayout(layout)
        self.threads = []

    def _start_http_client(self):
        http_client = HttpClient()
        http_client.map_signal.connect(self._write_to_screen)
        self.threads.append(http_client)
        http_client.start()

    def _write_to_screen(self, elevation_map):
        map_str = ""

        for x in range(len(elevation_map)):
            for y in range(len(elevation_map[0])):
                map_str += str(elevation_map[x][y])
            map_str += "\n"
        map_str += "\n"

        self.list_widget.addItem(unicode(map_str))

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
        :return: the cube in mesh format that pyqtgraph can understand
        :rtype: numpy array
        """

        p0 = [pos_x, pos_y, 0]
        p1 = [pos_x + res_x, pos_y, 0]
        p2 = [pos_x + res_x, pos_y + res_y, 0]
        p3 = [pos_x, pos_y + res_y, 0]
        p4 = [pos_x, pos_y, height]
        p5 = [pos_x + res_x, pos_y, height]
        p6 = [pos_x + res_x, pos_y + res_y, height]
        p7 = [pos_x, pos_y + res_y, height]

        constructed_cube = np.array(
            [[p0, p1, p2], [p0, p2, p3], [p4, p5, p6], [p4, p6, p7], [p0, p1, p5], [p0, p5, p4], [p1, p2, p6], [p1, p6, p5],
                [p2, p3, p7], [p2, p7, p6], [p0, p3, p7], [p0, p7, p4]])

        return constructed_cube
