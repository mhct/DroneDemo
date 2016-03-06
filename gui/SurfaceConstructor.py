
class SurfaceConstructor:
    def __init__(self):
        raise NotImplementedError("Never create an instance of this class.")

    @staticmethod
    def construct_drone(drone_position, res):
        # TODO add direction

        p0 = [drone_position.x + res.x / 2, drone_position.y + res.y / 2, drone_position.z]
        p1 = [drone_position.x - res.x / 2, drone_position.y + res.y / 2, drone_position.z]
        p2 = [drone_position.x - res.x / 2, drone_position.y - res.y / 2, drone_position.z]
        p3 = [drone_position.x + res.x / 2, drone_position.y - res.y / 2, drone_position.z]

        drone_shape = [[p0, p1, p2], [p0, p3, p2]]

        return drone_shape

    @staticmethod
    def construct_cube(pos_x, pos_y, res, height):
        """
        Construct the cube given its origin corner (the one with the smallest x and y values), the resolution of each
        cell and the height
        :param pos_x: x coordinate
        :type pos_x: int
        :param pos_y: y coordinate
        :type pos_y: int
        :param res: resolution in two coordinates (millimeters)
        :type res: Resolution
        :param height: the height of the cube
        :type height: int (millimeters)
        :return: the cube as a list of triangular surface in mesh format that pyqtgraph can understand
        :rtype: array
        """

        p0 = [pos_x, pos_y, 0]
        p1 = [pos_x + res.x, pos_y, 0]
        p2 = [pos_x + res.x, pos_y + res.y, 0]
        p3 = [pos_x, pos_y + res.y, 0]
        p4 = [pos_x, pos_y, height]
        p5 = [pos_x + res.x, pos_y, height]
        p6 = [pos_x + res.x, pos_y + res.y, height]
        p7 = [pos_x, pos_y + res.y, height]

        constructed_cube = [[p0, p1, p2], [p0, p2, p3], [p4, p5, p6], [p4, p6, p7], [p0, p1, p5], [p0, p5, p4],
                            [p1, p2, p6], [p1, p6, p5], [p2, p3, p7], [p2, p7, p6], [p0, p3, p7], [p0, p7, p4]]

        return constructed_cube
