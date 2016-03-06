import os
from functools import partial

import numpy as np
from PyQt4 import QtGui
import pyqtgraph.opengl as gl

from VirtualObject import VirtualObject
from gui.SurfaceConstructor import SurfaceConstructor


class Popup(QtGui.QWidget):
    def __init__(self, existing_object_ids, map_width, resolution, controller):
        """
        :param existing_object_ids: the list of ids of existing objects
        :type existing_object_ids: list of int
        :param controller: the controller
        :type controller: Controller
        """
        super(Popup, self).__init__()
        # a dictionary where keys are the object ids, values are object meshes
        self._mesh = {}

        self._map_width = map_width
        self._resolution = resolution
        self._controller = controller

        self._init_components(existing_object_ids)

    def _init_components(self, existing_object_ids):
        # use grid layout
        grid = self._init_grid_layout()

        self._init_checkboxes(existing_object_ids, grid)
        self._init_3d_preview(existing_object_ids, grid)
        self._init_buttons(grid)

        self.setLayout(grid)
        self.setGeometry(200, 50, 512, 360)
        self.show()

    def _init_buttons(self, grid):
        cancel_button = QtGui.QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        grid.addWidget(cancel_button, 11, 11)

        # TODO design preview
        update_button = QtGui.QPushButton("Update")
        update_button.clicked.connect(self._update_map)
        grid.addWidget(update_button, 11, 12)

    def _init_grid_layout(self):
        # TODO refactor duplicate code
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        return grid

    def _init_checkboxes(self, existing_object_ids, grid):
        scroll = QtGui.QScrollArea()

        all_checkboxes = QtGui.QWidget(scroll)
        layout = QtGui.QVBoxLayout(all_checkboxes)

        # TODO move this logic to controller?
        all_object_ids = [int(f[11]) for f in os.walk("../virtualobjects").next()[2] if f[0:11] == "main_object"]

        self._check_boxes = []
        for i in all_object_ids:
            checkbox = QtGui.QCheckBox("Object_" + str(i))
            layout.addWidget(checkbox)
            self._check_boxes.append(checkbox)
            if i in existing_object_ids:
                checkbox.toggle()
            checkbox.stateChanged.connect(partial(self._checkbox_changed, checkbox, i))

        scroll.setWidget(all_checkboxes)
        grid.addWidget(scroll, 0, 0, 2, 3)

    def _update_map(self):
        object_ids = []
        for checkbox in self._check_boxes:
            if checkbox.isChecked():
                object_ids.append(int(checkbox.text()[-1]))

        self._controller.set_map(object_ids)
        self.close()

    def _checkbox_changed(self, checkbox, virtual_object_id):
        if checkbox.isChecked():
            self._add_object(virtual_object_id)
        else:
            self._remove_object(virtual_object_id)

    def _init_3d_preview(self, existing_object_ids, grid):
        self._map_3d = gl.GLViewWidget()
        self._map_3d.setCameraPosition(distance=80 * (self._resolution.x + self._resolution.y) / 2)

        g = gl.GLGridItem()
        g.scale(self._resolution.x, self._resolution.y, (self._resolution.x + self._resolution.y) / 2)
        g.setSize(self._map_width.x, self._map_width.y)

        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 0, 3, 10, 10)

        for virtual_object_id in existing_object_ids:
            self._add_object(virtual_object_id)

    def _add_object(self, virtual_object_id):
        # if the mesh of this object has not been created before, create it
        if virtual_object_id not in self._mesh.keys():
            self._create_mesh(virtual_object_id)

        self._map_3d.addItem(self._mesh[virtual_object_id])

    def _create_mesh(self, virtual_object_id):
        virtual_object = VirtualObject("../virtualobjects/main_object" + str(virtual_object_id) + ".txt")

        surfaces = []
        for cell in virtual_object.get_cells():
            surfaces += SurfaceConstructor.construct_cube(cell.x * self._resolution.x, cell.y * self._resolution.y,
                                                          self._resolution, cell.height)

        object_mesh = gl.GLMeshItem(vertexes=np.array(surfaces), color=(0, 0, 1, 1), smooth=False, shader='shaded',
                                    glOptions='opaque')
        object_mesh.translate(-self._map_width.x * self._resolution.x / 2, -self._map_width.y * self._resolution.y / 2,
                              0, True)

        self._mesh[virtual_object_id] = object_mesh

    def _remove_object(self, virtual_object_id):
        self._map_3d.removeItem(self._mesh[virtual_object_id])
