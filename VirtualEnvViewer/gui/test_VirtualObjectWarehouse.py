from VirtualEnvViewer.gui.VirtualObjectWarehouse import VirtualObjectWarehouse


class TestVirtualObjectWarehouse:

    def method_setup(self, method):
        self._warehouse = VirtualObjectWarehouse("../resources_virtualobjects", "test_object")

    def test_instantiate(self):

        assert self._warehouse is not None

    def test_add_objects(self):
        pass