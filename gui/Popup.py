import os
from functools import partial

import numpy as np
from PyQt4 import QtGui
import pyqtgraph.opengl as gl

from VirtualObject import VirtualObject
from gui.DrawingHelper import DrawingHelper


class Popup(QtGui.QWidget):
    def __init__(self, map_width, resolution, controller):
        super(Popup, self).__init__()
        # a dictionary where keys are the file name, values are object meshes
        self._mesh = {}

        self._map_width = map_width
        self._resolution = resolution
        self._controller = controller

        self._init_components()

    def _init_components(self):
        # use grid layout
        grid = self._init_grid_layout()

        existing_object_hashcodes = self._controller.get_existing_object_hashcodes()
        self._init_3d_preview(grid)
        self._init_checkboxes(existing_object_hashcodes, grid)
        self._add_drone(self._controller.get_drone_pose())
        self._init_buttons(grid)

        self.setLayout(grid)
        self.setGeometry(200, 50, 512, 360)
        self.show()

    def _init_buttons(self, grid):
        cancel_button = QtGui.QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        grid.addWidget(cancel_button, 11, 11)

        update_button = QtGui.QPushButton("Update")
        update_button.clicked.connect(self._update_map)
        grid.addWidget(update_button, 11, 12)

    def _init_grid_layout(self):
        # TODO refactor duplicate code
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        return grid

    def _init_checkboxes(self, existing_object_hashcodes, grid):
        scroll = QtGui.QScrollArea()

        all_checkboxes = QtGui.QWidget(scroll)
        layout = QtGui.QVBoxLayout(all_checkboxes)

        object_file_names = self._controller.get_all_object_file_names()

        self._check_boxes = {}
        for file_name in object_file_names:
            checkbox = QtGui.QCheckBox(self._controller.get_object_by_file_name(file_name).get_name())
            layout.addWidget(checkbox)
            self._check_boxes[file_name] = checkbox
            checkbox.stateChanged.connect(partial(self._checkbox_changed, checkbox, file_name))

        for hashcode in existing_object_hashcodes:
            file_name = self._controller.get_file_name_by_hashcode(hashcode)
            self._check_boxes[file_name].toggle()

        scroll.setWidget(all_checkboxes)
        grid.addWidget(scroll, 0, 0, 2, 3)

    def _update_map(self):
        file_names = []
        for checkbox_key in self._check_boxes.keys():
            checkbox = self._check_boxes[checkbox_key]
            if checkbox.isChecked():
                file_names.append(checkbox_key)

        self._controller.set_map(file_names)
        self.close()

    def _checkbox_changed(self, checkbox, file_name):
        if checkbox.isChecked():
            self._add_object(file_name)
        else:
            self._remove_object(file_name)

    def _init_3d_preview(self, grid):
        self._map_3d = gl.GLViewWidget()
        self._map_3d.setCameraPosition(distance=80 * (self._resolution.x + self._resolution.y) / 2)

        g = gl.GLGridItem()
        g.scale(self._resolution.x, self._resolution.y, (self._resolution.x + self._resolution.y) / 2)
        g.setSize(self._map_width.x, self._map_width.y)

        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 0, 3, 10, 10)

    def _add_object(self, file_name):
        # if the mesh of this object has not been created before, create it
        if file_name not in self._mesh.keys():
            self._create_mesh(file_name)

        self._map_3d.addItem(self._mesh[file_name])

    def _add_drone(self, drone_state):
        drone_mesh = DrawingHelper.create_drone_mesh(drone_state, self._resolution)
        drone_mesh.translate(-self._map_width.x * self._resolution.x / 2, -self._map_width.y * self._resolution.y / 2,
                             0, True)
        self._map_3d.addItem(drone_mesh)

    def _create_mesh(self, file_name):
        virtual_object = self._controller.get_object_by_file_name(file_name)

        surfaces = []
        for cell in virtual_object.get_cells():
            surfaces += DrawingHelper.construct_cube(cell.x * self._resolution.x, cell.y * self._resolution.y,
                                                     self._resolution, cell.height)

        object_mesh = gl.GLMeshItem(vertexes=np.array(surfaces), color=(0, 0, 1, 1), smooth=False, shader='shaded',
                                    glOptions='opaque')
        object_mesh.translate(-self._map_width.x * self._resolution.x / 2, -self._map_width.y * self._resolution.y / 2,
                              0, True)

        self._mesh[file_name] = object_mesh

    def _remove_object(self, virtual_object_hashcode):
        self._map_3d.removeItem(self._mesh[virtual_object_hashcode])
