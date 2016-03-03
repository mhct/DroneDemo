from Obstacle import Obstacle
from Helper import Point


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
        # elevation map that stores the height of obstacles for quick querying, initialize all cells as 0
        self.elevation_map = [[0 for i in range(size_y)] for i in range(size_x)]

        # id map, each cell is a list that stores the id and the height of obstacles that occupied the cell,
        # is empty initially
        self.id_map = [[{} for i in range(size_y)] for i in range(size_x)]

        # the dictionary where key are obstacle ids, values are the obstacle objects
        self.obstacle_dict = {}

        # store cell resolution
        self.res_x = res_x
        self.res_y = res_y

    def add_obstacle(self, obstacle):
        """
        Add an obstacle to the environment
        :param obstacle: the obstacle to be added
        :type obstacle: Obstacle
        """
        self.obstacle_dict[obstacle.get_id()] = obstacle

        for cell in obstacle.get_cells():
            x = cell.x
            y = cell.y
            occupying_pieces = self.id_map[x][y]
            occupying_pieces[obstacle.get_id()] = cell.height
            # the height in the elevation map is of the highest obstacle
            self.elevation_map[x][y] = max(occupying_pieces.values())

    def is_in_obstacle_region(self, point):
        """
        Check whether a point is in obstacle region
        :param point: the point to be checked
        :type point: Point
        :return: True if the point is in obstacle region
        :rtype: bool
        """
        cell_x = int(point.x / self.res_x)
        cell_y = int(point.y / self.res_y)

        if self.elevation_map[cell_x][cell_y] >= point.z:
            return True
        else:
            return False

    def remove_obstacle(self, obstacle_id):
        """
        Remove an obstacle from map
        :param obstacle_id: the id of the obstacle to be removed
        :type obstacle_id: int
        """
        obstacle = self.obstacle_dict.pop(obstacle_id)
        for cell in obstacle.get_cells():
            x = cell.x
            y = cell.y

            # remove the occupying piece from the id map
            occupying_pieces = self.id_map[x][y]
            occupying_pieces.pop(obstacle_id)

            if len(occupying_pieces.values()) == 0:
                # no more obstacle, height is set to zero
                self.elevation_map[x][y] = 0
            else:
                self.elevation_map[x][y] = max(occupying_pieces.values())

    def clear_map(self):
        self._clear_elevation_map()
        self._clear_id_map()
        self._clear_obstacle_dict()

    def _clear_elevation_map(self):
        x = len(self.elevation_map)
        y = len(self.elevation_map[0])
        self.elevation_map = [[0 for i in range(y)] for i in range(x)]

    def _clear_id_map(self):
        x = len(self.id_map)
        y = len(self.id_map)
        self.id_map = [[{} for i in range(y)] for i in range(x)]

    def _clear_obstacle_dict(self):
        self.obstacle_dict = {}
