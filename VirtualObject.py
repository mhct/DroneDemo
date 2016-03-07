from collections import namedtuple

from Helper import Cell


class VirtualObject:
    """
    Immutable class to store virtual object information
    """

    def __init__(self, file_path):
        self._name = ""
        self._cells = frozenset()
        self._read_file(file_path)

    def get_cells(self):
        """
        :return: a list of cells that the object occupies
        :rtype: list
        """
        return self._cells

    def _read_file(self, file_path):
        """
        Read the object from a text file
        :param file_path: the path to the file
        :type file_path: str
        """

        f = open(file_path, 'r')

        # the first line of the input file defines the name of the object
        first_line = f.readline()
        self._name = first_line

        cells = []
        line = f.readline()
        # TODO detect invalid object here
        while line:
            data = [int(i) for i in line.split()]
            cells.append(Cell(data[0], data[1], data[2]))
            line = f.readline()

        f.close()

        self._cells = frozenset(cells)

    def get_name(self):
        """
        :return: the predefined name of the virtual object
        :rtype: str
        """
        return self._name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._name == other._name and self._cells == other._cells

    def __hash__(self):
        return hash((self._name, self._cells))
