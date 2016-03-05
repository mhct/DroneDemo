import os

import pyqtgraph.opengl as gl
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from HttpClient import HttpClient
from MapGetter import MapGetter
from MapSetter import MapSetter


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Initialize the http client
        self._http_client = HttpClient()
        # the gui
        self._init_gui()
        # the list to keep references to active threads
        self._threads = []
        # the mesh that represent the environment
        self._mesh = None
        # the map setter TODO need to be refactored
        self._map_setter = MapSetter(self._http_client)

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
        self._init_object_checkbox(grid)

        # set the layout
        self.setLayout(grid)
        # position x, position y, width, height
        self.setGeometry(100, 0, 1024, 720)
        self.show()

    def _init_object_checkbox(self, grid):
        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        all_checkboxes = QtGui.QWidget(scroll)
        layout = QtGui.QVBoxLayout(all_checkboxes)
        file_count = len([f for f in os.walk("../virtualobjects").next()[2] if f[0:11] == "main_object"])

        self._check_boxes = []
        for i in range(1, file_count + 1):
            checkbox = QtGui.QCheckBox("Object_" + str(i))
            layout.addWidget(checkbox)
            self._check_boxes.append(checkbox)

        scroll.setWidget(all_checkboxes)
        grid.addWidget(scroll, 4, 0, 2, 3)

    def _init_3d_map(self, grid):
        self._map_3d = gl.GLViewWidget()
        res = self._http_client.get_resolution()
        self._map_3d.setCameraPosition(distance=80 * (res.x + res.y) / 2)
        g = gl.GLGridItem()
        g.scale(res.x, res.y, (res.x + res.y) / 2)
        # TODO use variable here
        g.setSize(50, 50, 50)
        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 1, 3, 10, 10)

    def _init_list_widget(self, grid):
        self.list_widget = QtGui.QListWidget()
        grid.addWidget(self.list_widget, 13, 3, 3, 10)

    # noinspection PyUnresolvedReferences
    def _init_buttons(self, grid):
        connect_button = QtGui.QPushButton("Connect")
        connect_button.clicked.connect(self._start_map_getter)
        grid.addWidget(connect_button, 1, 0)

        set_button = QtGui.QPushButton("Set")
        set_button.clicked.connect(self._set_map)
        grid.addWidget(set_button, 3, 0)

        # TODO design preview
        preview_button = QtGui.QPushButton("Preview")
        grid.addWidget(preview_button, 3, 1)

    def _init_grid_layout(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        return grid

    def _set_map(self):
        object_ids = []

        for checkbox in self._check_boxes:
            if checkbox.isChecked():
                object_ids.append(int(checkbox.text()[-1]))

        self._map_setter.set_map(object_ids)

    def _start_map_getter(self):
        """
        Initialize a thread that gets the map from the drones and visualize it for each second
        """
        # TODO prevent this one from being called twice
        map_getter = MapGetter(self._http_client)
        map_getter.map_signal.connect(self._draw_3d_map)
        self._threads.append(map_getter)
        map_getter.start()

    def _write_to_screen(self, message):
        self.list_widget.addItem(unicode(message))

    def _draw_3d_map(self, mesh):
        if self._mesh is not None:
            self._map_3d.removeItem(self._mesh)

        self._mesh = mesh
        if self._mesh is not None:
            self._map_3d.addItem(self._mesh)

        self._write_to_screen("updated map")
