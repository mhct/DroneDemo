import os

import pyqtgraph.opengl as gl
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from gui.Popup import Popup


class View(QtGui.QWidget):
    def __init__(self, map_width, resolution, controller):
        """
        :param map_width The width of the map in three coordinates
        :type map_width: MapWidth
        :param resolution: The resolution of each cell of the map in three coordinates
        :type resolution: Resolution
        :param controller: the controller
        :type controller: Controller
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
        self._init_console(grid)
        self._init_3d_map(grid)
        self._init_object_list_console(grid)

        # set the layout
        self.setLayout(grid)
        # position x, position y, width, height
        self.setGeometry(100, 0, 1024, 720)
        self.show()

    def _init_object_list_console(self, grid):
        self._object_list_console = QtGui.QListWidget()
        grid.addWidget(self._object_list_console, 4, 0, 2, 3)

    def _init_3d_map(self, grid):
        self._map_3d = gl.GLViewWidget()
        self._map_3d.setCameraPosition(distance=80 * (self._resolution.x + self._resolution.y) / 2)

        g = gl.GLGridItem()
        g.scale(self._resolution.x, self._resolution.y, (self._resolution.x + self._resolution.y) / 2)
        g.setSize(self._map_width.x, self._map_width.y)

        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 1, 3, 10, 10)

    def _init_console(self, grid):
        self._console = QtGui.QListWidget()
        grid.addWidget(self._console, 13, 3, 3, 10)

    # noinspection PyUnresolvedReferences
    def _init_buttons(self, grid):
        update_map_button = QtGui.QPushButton("Update Map")
        update_map_button.clicked.connect(self._open_popup)
        grid.addWidget(update_map_button, 3, 0)

    def _open_popup(self):
        self._popup = Popup(self._controller.get_existing_object_ids(), self._map_width, self._resolution,
                            self._controller)

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
        self._console.addItem(unicode(message))

    def draw_objects_and_drone(self, mesh):
        self._remove_previous_mesh()
        self._update_stored_mesh(mesh)
        self._add_new_virtual_object_mesh()
        self._add_new_drone_mesh()
        self._write_to_screen("updated map")

    def _update_stored_mesh(self, mesh):
        self._mesh = mesh

    def _add_new_drone_mesh(self):
        if self._mesh.drone is not None:
            self._mesh.drone.translate(-self._map_width.x * self._resolution.x / 2,
                                       -self._map_width.y * self._resolution.y / 2, 0, True)
            self._map_3d.addItem(self._mesh.drone)

    def _add_new_virtual_object_mesh(self):
        if self._mesh.virtual_objects is not None:
            self._mesh.virtual_objects.translate(-self._map_width.x * self._resolution.x / 2,
                                                 -self._map_width.y * self._resolution.y / 2, 0, True)
            self._map_3d.addItem(self._mesh.virtual_objects)

    def _remove_previous_mesh(self):
        if self._mesh is not None:
            if self._mesh.virtual_objects is not None:
                self._map_3d.removeItem(self._mesh.virtual_objects)

            if self._mesh.drone is not None:
                self._map_3d.removeItem(self._mesh.drone)

    def update_list_object_ids(self, object_ids):
        self._object_list_console.clear()
        for object_id in object_ids:
            self._object_list_console.addItem(unicode("Object_" + str(object_id)))
