from functools import partial
from PyQt4 import QtGui

import numpy as np

import pyqtgraph.opengl as gl
from gui.DrawingHelper import DrawingHelper
from CustomizedGLGridItem import CustomizedGLGridItem


class Popup(QtGui.QWidget):
    def __init__(self, map_params, controller):
        super(Popup, self).__init__()
        # a dictionary where keys are the virtual objects, values are the corresponding meshes
        self._mesh = {}

        self._map_params = map_params
        self._controller = controller

        self._init_components()

    def _init_components(self):
        # use grid layout
        grid = self._init_grid_layout()

        self._init_3d_preview(grid)
        self._init_checkboxes(grid)
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

    def _init_checkboxes(self, grid):
        scroll = QtGui.QScrollArea()

        all_checkboxes = QtGui.QWidget(scroll)
        layout = QtGui.QVBoxLayout(all_checkboxes)

        objects_in_warehouse = self._controller.get_all_objects_in_warehouse()

        self._check_boxes = {}
        for virtual_object in objects_in_warehouse:
            self._create_checkbox(layout, virtual_object)

        added_objects = self._controller.get_added_objects()
        for virtual_object in added_objects:
            self._check_boxes[virtual_object].toggle()

        scroll.setWidget(all_checkboxes)
        grid.addWidget(scroll, 0, 0, 2, 3)

    def _create_checkbox(self, layout, virtual_object):
        checkbox = QtGui.QCheckBox(virtual_object.get_name())
        layout.addWidget(checkbox)
        self._check_boxes[virtual_object] = checkbox
        checkbox.stateChanged.connect(partial(self._checkbox_changed, checkbox, virtual_object))

    def _update_map(self):
        selected_objects = self._get_selected_objects()
        self._controller.set_map(selected_objects)
        self.close()

    def _get_selected_objects(self):
        selected_objects = []

        for virtual_object in self._check_boxes.keys():
            checkbox = self._check_boxes[virtual_object]
            if checkbox.isChecked():
                selected_objects.append(virtual_object)

        return selected_objects

    def _checkbox_changed(self, checkbox, virtual_object):
        if checkbox.isChecked():
            self._add_object(virtual_object)
        else:
            self._remove_object(virtual_object)

    def _init_3d_preview(self, grid):
        res = self._map_params.resolution
        width = self._map_params.map_width

        self._map_3d = gl.GLViewWidget()
        self._map_3d.setCameraPosition(distance=80 * (res.x + res.y) / 2)
        self._map_3d.setBackgroundColor('w')

        g = CustomizedGLGridItem()
        g.scale(res.x, res.y, (res.x + res.y) / 2)
        g.setSize(width.x, width.y)

        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 0, 3, 10, 10)

    def _add_object(self, virtual_object):
        # if the mesh of this object has not been created before, create it
        if virtual_object not in self._mesh.keys():
            self._create_mesh(virtual_object)

        self._map_3d.addItem(self._mesh[virtual_object])

    def _add_drone(self, drone_state):
        if drone_state is None:
            return

        res = self._map_params.resolution
        width = self._map_params.map_width

        drone_mesh = DrawingHelper.create_drone_mesh(drone_state, res)
        for item in drone_mesh:
            item.translate(-width.x * res.x / 2, -width.y * res.y / 2, 0, True)
            self._map_3d.addItem(item)

    def _create_mesh(self, virtual_object):
        res = self._map_params.resolution
        width = self._map_params.map_width
        color = virtual_object.get_color()

        surfaces = []
        for cell in virtual_object.get_cells():
            surfaces += DrawingHelper.construct_cube(cell.x * res.x, cell.y * res.y, res, cell.height)

        object_mesh = gl.GLMeshItem(vertexes=np.array(surfaces), color=color, smooth=False, shader='shaded',
                                    glOptions='opaque')
        object_mesh.translate(-width.x * res.x / 2, -width.y * res.y / 2, 0, True)

        self._mesh[virtual_object] = object_mesh

    def _remove_object(self, virtual_object):
        self._map_3d.removeItem(self._mesh[virtual_object])
