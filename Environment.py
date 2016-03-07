from CellData import CellData
from VirtualObject import VirtualObject
from Helper import Point, Resolution, MapWidth, MapParams, Cell


class Environment:
    """
    Model of the environment.
    """

    def __init__(self, map_width, resolution):
        """
        Initialize an empty map and an empty list of objects.
        :param map_width: the width of the map in x and y (or the number of cells in each row and each column)
        :type map_width: __namedtuple MapWidth
        :param resolution: the resolution of each cell in x and y
        :type resolution: __namedtuple Resolution
        :return:
        :rtype:
        """
        # store cell resolution
        self._res = resolution

        # store the map width
        self._map_width = map_width

        # the grid map
        self._grid_map = [[CellData() for i in range(self._map_width.x)] for i in range(self._map_width.y)]

        # the dictionary where key are object hash code, values are the object instance
        self._object_dict = {}

    def add_virtual_object(self, virtual_object):
        """
        Add an object to the environment, return the hashcode of the object on the server
        :param virtual_object: the object to be added
        :type virtual_object: VirtualObject
        :return the hashcode of the object on the server
        :rtype hashcode
        """
        virtual_object_hash = hash(virtual_object)

        if virtual_object_hash in self._object_dict.keys():
            raise ValueError("The object is already added to the grid map")

        self._object_dict[virtual_object_hash] = virtual_object

        for cell in virtual_object.get_cells():
            x = cell.x
            y = cell.y
            self._grid_map[x][y].add_virtual_object(virtual_object, cell.height)

        return virtual_object_hash

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

    def remove_virtual_object_by_hashcode(self, hashcode):
        virtual_object = self._object_dict.pop(hashcode)

        for cell in virtual_object.get_cells():
            x = cell.x
            y = cell.y
            self._grid_map[x][y].remove_virtual_object(virtual_object)

    def remove_virtual_object(self, virtual_object):
        """
        Remove an object from map
        :param virtual_object: the the object to be removed
        :type virtual_object: VirtualObject
        """
        self.remove_virtual_object_by_hashcode(hash(virtual_object))

    def clear_map(self):
        for x in range(self._map_width.x):
            for y in range(self._map_width.y):
                self._grid_map[x][y].clear_cell()

    def get_elevation_map(self):
        cells = []
        for x in range(self._map_width.x):
            for y in range(self._map_width.y):
                cells.append(Cell(x, y, self._grid_map[x][y].get_max_height()))
        return cells

    def get_map_params(self):
        return MapParams(self._map_width, self._res)

    def get_all_object_hashcodes(self):
        """
        :return: the list of hashcodes of all objects currently in the environment
        :rtype: list of int
        """
        return self._object_dict.keys()
