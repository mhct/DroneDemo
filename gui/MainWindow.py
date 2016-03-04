import numpy as np
from PyQt4 import QtGui
import pyqtgraph.opengl as gl

from MapUpdater import MapUpdater
from HttpClient import HttpClient


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._http_client = HttpClient()
        self._init_gui()
        # the list to keep references to active threads
        self.threads = []

    def _init_gui(self):
        """
        Initialize the gui
        """
        # use grid layout
        grid = self._init_grid_layout()

        # initialize components
        self._init_buttons(grid)
        self._init_list_widget(grid)
        self._init_3d_map(grid)

        # set the layout
        self.setLayout(grid)
        # position x, position y, width, height
        self.setGeometry(300, 0, 1024, 720)
        self.show()

    def _init_3d_map(self, grid):
        self.map_3d = gl.GLViewWidget()
        self.map_3d.setCameraPosition(distance=100)
        g = gl.GLGridItem()
        g.scale(1, 1, 1)
        g.setSize(50, 50, 50)
        self.map_3d.addItem(g)
        grid.addWidget(self.map_3d, 2, 0, 10, 10)

    def _init_list_widget(self, grid):
        self.list_widget = QtGui.QListWidget()
        grid.addWidget(self.list_widget, 13, 0, 3, 10)

    def _init_buttons(self, grid):
        self.button = QtGui.QPushButton("Connect")
        self.button.clicked.connect(self._start_map_updater)
        grid.addWidget(self.button, 1, 0)

    def _init_grid_layout(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        return grid

    def _start_map_updater(self):
        # TODO prevent this one from being called twice
        map_updater = MapUpdater(self._http_client)
        map_updater.map_signal.connect(self._draw_3d_map)
        self.threads.append(map_updater)
        map_updater.start()

    def _write_to_screen(self, message):
        self.list_widget.addItem(unicode(message))

    def _draw_3d_map(self, mesh):
        # TODO remove old items
        self.map_3d.addItem(mesh)
        self._write_to_screen("updated map")
