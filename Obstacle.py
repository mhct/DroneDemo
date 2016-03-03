from collections import namedtuple

from Helper import Cell


class Obstacle:
    def __init__(self, file_path):
        self._id = -1
        self._cells = []
        self._read_file(file_path)

    def get_cells(self):
        return self._cells

    def _read_file(self, file_path):
        if self._id != -1:
            raise Exception("Obstacle is already initialized")

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
