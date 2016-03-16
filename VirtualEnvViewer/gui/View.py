from PyQt4 import QtGui

import pyqtgraph.opengl as gl
from VirtualEnvViewer.gui import Controller
from DrawingHelper import DrawingHelper
from Popup import Popup


class View(QtGui.QWidget):
    def __init__(self, controller):
        """
        :param controller: the controller
        :type controller: Controller
        """
        super(View, self).__init__()

        self._controller = controller
        self._controller.drone_pose_update_signal.connect(self._update_drone_pose)
        self._controller.virtual_env_update_signal.connect(self._update_virtual_environment)

        # get the parameter of the map to be displayed
        self._map_params = self._controller.get_map_params()

        # initialize gui components
        self._init_components()

        # store the previous mesh locally
        self._drone_mesh = None
        self._elevation_map_mesh = None

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
        self._update_added_object_list(self._controller.get_added_objects())
        grid.addWidget(self._object_list_console, 1, 0, 2, 3)

    def _update_added_object_list(self, virtual_objects):
        self._object_list_console.clear()
        for obj in virtual_objects:
            self._object_list_console.addItem(unicode(obj.get_name()))

    # noinspection PyUnresolvedReferences
    def _init_buttons(self, grid):
        update_map_button = QtGui.QPushButton("Update Map")
        update_map_button.clicked.connect(self._open_popup)
        grid.addWidget(update_map_button, 0, 0, 1, 3)

    def _init_3d_map(self, grid):
        res = self._map_params.resolution
        width = self._map_params.map_width

        self._map_3d = gl.GLViewWidget()
        self._map_3d.setCameraPosition(distance=80 * (res.x + res.y) / 2)

        g = gl.GLGridItem()
        g.scale(res.x, res.y, (res.x + res.y) / 2)
        g.setSize(width.x, width.y)

        self._map_3d.addItem(g)
        grid.addWidget(self._map_3d, 0, 3, 10, 10)

    def _init_console(self, grid):
        self._console = QtGui.QListWidget()
        grid.addWidget(self._console, 13, 3, 3, 10)

    def _open_popup(self):
        self._popup = Popup(self._map_params, self._controller)

    def _init_grid_layout(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        return grid

    def _write_to_console(self, message):
        self._console.addItem(unicode(message))

    def _draw_objects_and_drone(self, mesh):
        self._remove_previous_mesh()
        self._update_stored_mesh(mesh)
        self._add_new_virtual_object_mesh()
        self._add_new_drone_mesh()
        self._write_to_console("updated map")

    def _draw_new_drone_pose(self, drone_mesh):
        # remove previous drone_mesh
        if self._drone_mesh is not None:
            self._map_3d.removeItem(self._drone_mesh)

        self._drone_mesh = drone_mesh

        res = self._map_params.resolution
        width = self._map_params.map_width

        if self._drone_mesh is not None:
            self._drone_mesh.translate(-width.x * res.x / 2, -width.y * res.y / 2, 0, True)
            self._map_3d.addItem(self._drone_mesh)

    def _draw_new_elevation_map(self, elevation_map_mesh):
        if self._elevation_map_mesh is not None:
            self._map_3d.removeItem(self._elevation_map_mesh)

        res = self._map_params.resolution
        width = self._map_params.map_width

        self._elevation_map_mesh = elevation_map_mesh
        if self._elevation_map_mesh is not None:
            self._elevation_map_mesh.translate(-width.x * res.x / 2, -width.y * res.y / 2, 0, True)
            self._map_3d.addItem(self._elevation_map_mesh)

    def _update_drone_pose(self):
        drone_pose = self._controller.get_drone_pose()

        if drone_pose is None:
            return

        drone_mesh = DrawingHelper.create_drone_mesh(drone_pose, self._map_params.resolution)
        self._draw_new_drone_pose(drone_mesh)

    def _update_virtual_environment(self):
        virtual_enviroment_objects = self._controller.get_added_objects()
        elevation_map_mesh = DrawingHelper.create_elevation_map_mesh(virtual_enviroment_objects,
                                                                     self._map_params.resolution)
        self._draw_new_elevation_map(elevation_map_mesh)
        self._update_added_object_list(virtual_enviroment_objects)
