from collections import namedtuple

from Helper import Cell


class VirtualObject:
    def __init__(self, file_path):
        # initially, the id is set to -1, which means the object is not initialized. If the object was initialized,
        # the id must be >= 0
        self._id = -1
        self._cells = []
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
        if self._id != -1:
            raise Exception("Object is already initialized")

        f = open(file_path, 'r')

        line = f.readline()
        self._id = int(line)

        self._cells = []

        line = f.readline()
        while line:
            data = [int(i) for i in line.split()]
            self._cells.append(Cell(data[0], data[1], data[2]))
            line = f.readline()

        f.close()

    def get_id(self):
        return self._id
