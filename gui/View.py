import os

import pyqtgraph.opengl as gl
from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class View(QtGui.QWidget):
    def __init__(self, map_width, resolution, controller):
        """
        :param map_width The width of the map in three coordinates
        :type map_width: MapWidth
        :param resolution: The resolution of each cell of the map in three coordinates
        :type resolution: Resolution
        """
        super(View, self).__init__()
        self._map_width = map_width
        self._resolution = resolution
        self._controller = controller
        # initialize gui components
        self._init_components()
        # store the previous mesh locally
        self._mesh = None

    def _init_components(self):
        """
        Initialize the gui components
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

        # TODO move this logic to controller?
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
        self._map_3d.setCameraPosition(distance=80 * (self._resolution.x + self._resolution.y) / 2)

        g = gl.GLGridItem()
        g.scale(self._resolution.x, self._resolution.y, (self._resolution.x + self._resolution.y) / 2)
        g.setSize(self._map_width.x, self._map_width.y)

        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 1, 3, 10, 10)

    def _init_list_widget(self, grid):
        self.list_widget = QtGui.QListWidget()
        grid.addWidget(self.list_widget, 13, 3, 3, 10)

    # noinspection PyUnresolvedReferences
    def _init_buttons(self, grid):
        set_button = QtGui.QPushButton("Set")
        set_button.clicked.connect(self._controller.set_map)
        grid.addWidget(set_button, 3, 0)

        # TODO design preview
        preview_button = QtGui.QPushButton("Preview")
        grid.addWidget(preview_button, 3, 1)

    def _init_grid_layout(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        return grid

    def get_checked_boxes(self):
        """
        :return: a list of checked boxes
        :rtype: list of checked boxes
        """
        checked_boxes = []

        for checkbox in self._check_boxes:
            if checkbox.isChecked():
                checked_boxes.append(checkbox)

        return checked_boxes

    def _write_to_screen(self, message):
        self.list_widget.addItem(unicode(message))

    def draw_3d_map(self, mesh):
        if self._mesh is not None:
            if self._mesh.virtual_objects is not None:
                self._map_3d.removeItem(self._mesh.virtual_objects)

            if self._mesh.drone is not None:
                self._map_3d.removeItem(self._mesh.drone)

        self._mesh = mesh
        if self._mesh.virtual_objects is not None:
            self._mesh.virtual_objects.translate(-self._map_width.x * self._resolution.x / 2,
                                                 -self._map_width.y * self._resolution.y / 2, 0, True)
            self._map_3d.addItem(self._mesh.virtual_objects)

        if self._mesh.drone is not None:
            self._mesh.drone.translate(-self._map_width.x * self._resolution.x / 2,
                                       -self._map_width.y * self._resolution.y / 2, 0, True)
            self._map_3d.addItem(self._mesh.drone)

        self._write_to_screen("updated map")
