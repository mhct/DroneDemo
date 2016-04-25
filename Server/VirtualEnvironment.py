from CellData import CellData
from VirtualObject import VirtualObject
from Helper import Point, MapParams, Cell


class VirtualEnvironment:
    """
    Model of the environment.
    """

    def __init__(self, map_params):
        """
        Initialize an empty map and an empty list of objects.
        :param map_params: Map parameters (Width and Resolution) the width of the map in x and y (or the number of cells in each row and each column)
        map_width: __namedtuple MapWidth
        cell_size: the size in millimeters of each cell in x and y
        """
        # store cell resolution
        self._res = map_params.resolution

        # store the map width
        self._map_width = map_params.map_width

        # the grid map
        self._grid_map = [[CellData() for i in range(self._map_width.x)] for i in range(self._map_width.y)]

        # set of existing virtual object
        self._virtual_object_set = set()

    def add_virtual_object(self, virtual_object):
        """
        Add an object to the environment, return the hashcode of the object on the server
        :param virtual_object: the object to be added
        :type virtual_object: VirtualObject
        :return the hashcode of the object on the server
        :rtype hashcode
        """
        if virtual_object in self._virtual_object_set:
            raise ValueError("The object is already added to the grid map")

        self._virtual_object_set.add(virtual_object)

        for cell in virtual_object.get_cells():
            x = cell.x
            y = cell.y
            self._grid_map[x][y].add_virtual_object(virtual_object, cell.height)

    def is_occupied(self, point):
        """
        Check whether a point in the environment is occupied by objects
        :param point: the point to be checked
        :type point: Point
        :return: True if the point is occupied by objects
        :rtype: bool
        """
        x = int(point.x / self._res.x)
        y = int(point.y / self._res.y)

        if x < 0 or x >= self._map_width.x or y < 0 or y >= self._map_width.y:
            raise ValueError("The input point is not in the modeled region.")

        return self._grid_map[x][y].is_occupied(point.z)

    def remove_virtual_object(self, virtual_object):
        """
        Remove an object from map
        :param virtual_object: the the object to be removed
        :type virtual_object: VirtualObject
        """
        if virtual_object in self._virtual_object_set:
            self._virtual_object_set.remove(virtual_object)

            for cell in virtual_object.get_cells():
                x = cell.x
                y = cell.y
                self._grid_map[x][y].remove_virtual_object(virtual_object)

            return True
        else:
            return False

    def clear_map(self):
        self._virtual_object_set.clear()

        for x in range(self._map_width.x):
            for y in range(self._map_width.y):
                self._grid_map[x][y].clear_cell()

    def _get_elevation_map(self):
        cells = []
        for x in range(self._map_width.x):
            for y in range(self._map_width.y):
                cells.append(Cell(x, y, self._grid_map[x][y].get_max_height()))
        return cells

    def get_map_params(self):
        return MapParams(self._map_width, self._res)

    def get_virtual_objects(self):
        ret = []

        for vo in self._virtual_object_set:
            data = dict()
            data["cells"] = vo.get_cells()
            data["name"] = vo.get_name()
            ret.append(data)

        return ret
