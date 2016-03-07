from VirtualObject import VirtualObject


class CellData:
    """
    This class hold the information stored in each cell of the grid map
    """

    def __init__(self):
        #  the maximum height of all object pieces occupying the cell
        self._max_height = 0
        # the dictionary where keys are the virtual object hash code, values are the heights of the pieces of objects
        self._object_height = {}

    def add_virtual_object(self, virtual_object, height):
        """
        Add an object piece to the cell
        :param virtual_object: the virtual object to be added
        :type virtual_object: VirtualObject
        :param height: the height of the virtual object at this cell
        :type height: float
        """
        # TODO improve the interface
        virtual_object_hash = hash(virtual_object)

        if virtual_object_hash in self._object_height.keys():
            raise ValueError("The object is already added to the cell.")

        self._object_height[virtual_object_hash] = height
        self._max_height = max(self._object_height.values())

    def remove_virtual_object(self, virtual_object):
        """
        Remove the virtual object from the cell
        :param virtual_object: the virtual object to be removed
        :type virtual_object: VirtualObject
        """
        virtual_object_hash = hash(virtual_object)
        self._object_height.pop(virtual_object_hash)

        if not any(self._object_height):
            # if there is no object in the cell
            self._max_height = 0
        else:
            self._max_height = max(self._object_height.values())

    def is_occupied(self, height):
        """
        Check whether the input height is occupied by objects
        :param height: the height to be checked
        :type height: float
        :return: true if the height is smaller than or equal to the maximum occupied height
        :rtype: bool
        """
        return height <= self._max_height

    def clear_cell(self):
        self._max_height = 0
        self._object_height = {}

    def get_max_height(self):
        return self._max_height
