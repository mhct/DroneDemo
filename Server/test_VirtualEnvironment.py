from VirtualObject import VirtualObject
from VirtualEnvironment import VirtualEnvironment
from Helper import Point, MapWidth, CellSize, MapParams


class TestVirtualEnvironment:
    def setup_method(self, method):
        self.env = VirtualEnvironment(MapParams(MapWidth(4, 4), CellSize(100, 100)))  # size_x size_y res_x res_y
        self._virtual_object1 = VirtualObject([[1, 1, 1000], [1, 2, 1000], [1, 3, 1000]])
        self._virtual_object2 = VirtualObject([[1, 0, 2000], [1, 2, 500], [1, 3, 2000]])

    def test_add_object_simple(self):
        vo = VirtualObject([[1, 1, 333]])
        self.env.add_virtual_object(vo)

        assert len(self.env.get_virtual_objects()) == 1

    def test_add_object(self):
        vo = VirtualObject([[0, 0, 100]])
        self.env.add_virtual_object(vo)

        assert self.env.is_occupied(Point(0, 0, 3)) is True

    def test_add_two_objects(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)

        assert self.env.is_occupied(Point(150, 50, 1999)) is True
        assert self.env.is_occupied(Point(150, 50, 2001)) is False

        assert self.env.is_occupied(Point(150, 150, 999)) is True
        assert self.env.is_occupied(Point(150, 150, 1001)) is False

        assert self.env.is_occupied(Point(150, 250, 999)) is True
        assert self.env.is_occupied(Point(150, 250, 1001)) is False

        assert self.env.is_occupied(Point(150, 350, 1999)) is True
        assert self.env.is_occupied(Point(150, 350, 2001)) is False

    def test_remove_object_case1(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.remove_virtual_object(self._virtual_object1)

        assert self.env.is_occupied(Point(150, 150, 500)) is False
        assert self.env.is_occupied(Point(150, 250, 500)) is False
        assert self.env.is_occupied(Point(150, 350, 500)) is False
        assert self.env.is_occupied(Point(50, 150, 500)) is False

    def test_remove_object_case2(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)
        self.env.remove_virtual_object(self._virtual_object2)

        assert self.env.is_occupied(Point(150, 150, 999)) is True
        assert self.env.is_occupied(Point(150, 150, 1001)) is False

        assert self.env.is_occupied(Point(150, 250, 999)) is True
        assert self.env.is_occupied(Point(150, 250, 1001)) is False

        assert self.env.is_occupied(Point(150, 350, 999)) is True
        assert self.env.is_occupied(Point(150, 350, 1001)) is False

        assert self.env.is_occupied(Point(50, 150, 1)) is False

    def test_clear_map(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)
        self.env.clear_map()
        assert len(self.env.get_virtual_objects()) == 0

    def test_add_retrieve_object(self):
        self.env.add_virtual_object(self._virtual_object1)
        assert len(self.env.get_virtual_objects()) == 1

    def test_add_retrieve_multiple_objects(self):
        self.env.add_virtual_object(self._virtual_object1)
        self.env.add_virtual_object(self._virtual_object2)

        assert len(self.env.get_virtual_objects()) == 2
