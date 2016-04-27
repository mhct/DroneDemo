from Helper import Cell

class VirtualObject:
    """
    Immutable class to store virtual object information
    """

    def __init__(self, cells, name):
        self._name = name
        if not len(cells) > 0:
            raise ValueError("There should be a list of Cells (x,y,z)")


        cellList = []

        for cell in cells:
            cellList.append(Cell(cell[0], cell[1], cell[2]))

        self._set_cells(cellList)

    def get_cells(self):
        """
        :return: a list of cells that the object occupies
        :rtype: list
        """
        return list(self._cells)

    def _set_cells(self, cells):
        self._cells = frozenset(cells)

    def get_name(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._name == other._name and self._cells == other._cells

    def __hash__(self):
        return hash((self._name, frozenset(self._cells)))

    def __str__(self):
        for cell in self._cells:
            print cell
