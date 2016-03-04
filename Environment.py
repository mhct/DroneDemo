from VirtualObject import VirtualObject
from Helper import Point, Resolution


class Environment:
    """
    Model of the environment.
    """

    def __init__(self, size_x, size_y, res_x, res_y):
        """
        Initialize an empty map and an empty list of objects.

        :param size_x: number of cells in x axis
        :type size_x: int
        :param size_y: number of cells in y axis
        :type size_y: int
        :param res_x: the resolution of one cell in x axis (in millimeters)
        :type res_x: int
        :param res_y: the resolution of one cell in y axis (in millimeters)
        :type res_y: int
        """
        # elevation map that stores the height of objects for quick querying, initialize all cells as 0
        self._elevation_map = [[0 for i in range(size_y)] for i in range(size_x)]

        # id map, each cell is a list that stores the id and the height of objects that occupied the cell,
        # is empty initially
        self._id_map = [[{} for i in range(size_y)] for i in range(size_x)]

        # the dictionary where key are object ids, values are the object instance
        self._object_dict = {}

        # store cell resolution
        self._res = Resolution(res_x, res_y)

    def add_virtual_object(self, virtual_object):
        """
        Add an object to the environment
        :param virtual_object: the object to be added
        :type virtual_object: VirtualObject
        """
        self._object_dict[virtual_object.get_id()] = virtual_object

        for cell in virtual_object.get_cells():
            x = cell.x
            y = cell.y
            occupying_pieces = self._id_map[x][y]
            occupying_pieces[virtual_object.get_id()] = cell.height
            # the height in the elevation map is of the highest object
            self._elevation_map[x][y] = max(occupying_pieces.values())

    def is_in_object_region(self, point):
        """
        Check whether a point is in object region
        :param point: the point to be checked
        :type point: Point
        :return: True if the point is in object region
        :rtype: bool
        """
        cell_x = int(point.x / self._res_x)
        cell_y = int(point.y / self._res_y)

        if self._elevation_map[cell_x][cell_y] >= point.z:
            return True
        else:
            return False

    def remove_virtual_object(self, virtual_object_id):
        """
        Remove an object from map
        :param virtual_object_id: the id of the object to be removed
        :type virtual_object_id: int
        """
        virtual_object = self._object_dict.pop(virtual_object_id)
        for cell in virtual_object.get_cells():
            x = cell.x
            y = cell.y

            # remove the occupying piece from the id map
            occupying_pieces = self._id_map[x][y]
            occupying_pieces.pop(virtual_object_id)

            if len(occupying_pieces.values()) == 0:
                # no more object, height is set to zero
                self._elevation_map[x][y] = 0
            else:
                self._elevation_map[x][y] = max(occupying_pieces.values())

    def clear_map(self):
        self._clear_elevation_map()
        self._clear_id_map()
        self._clear_object_dict()

    def _clear_elevation_map(self):
        x = len(self._elevation_map)
        y = len(self._elevation_map[0])
        self._elevation_map = [[0 for i in range(y)] for i in range(x)]

    def _clear_id_map(self):
        x = len(self._id_map)
        y = len(self._id_map)
        self._id_map = [[{} for i in range(y)] for i in range(x)]

    def _clear_object_dict(self):
        self._object_dict = {}

    def get_elevation_map(self):
        return self._elevation_map

    def get_resolution(self):
        return self._res