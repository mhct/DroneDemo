import os
from VirtualObject import VirtualObject


class VirtualObjectWarehouse:
    """
    The warehouse storing virtual objects
    """

    def __init__(self):
        self._all_objects = set()
        self._outside_virtual_environment_objects = set()
        self._virtual_environment_objects = set()

    def get_all_objects(self):
        return self._all_objects

    def get_virtual_environment_objects(self):
        return self._virtual_environment_objects

    def add_outside_virtual_environment_objects(self, virtual_object):
        self._outside_virtual_environment_objects.add(virtual_object)
        self._update_all_objects()

    def replace_virtual_environment_objects(self, virtual_objects):
        if not isinstance(virtual_objects, set):
            raise ValueError("Should be a list of Virtual Objects")

        self._virtual_environment_objects = set(virtual_objects)
        self._update_all_objects()

    def _update_all_objects(self):
        self._all_objects = self._all_objects.union(self._outside_virtual_environment_objects)
        self._all_objects = self._all_objects.union(self._virtual_environment_objects)


class LocalLoaderVirtualObjects:
    def load_virtual_objects(directory, prefix):
        """
        Scan all input files whose names starting with the given prefix, create virtual object from those files and
        store them in a set.
        :param directory: the directory to be scanned
        :type directory: str
        :param prefix: the prefix
        :type prefix: str
        :return: a set of virtual objects
        """
        file_list = [f for f in os.walk(directory).next()[2] if f.startswith(prefix)]

        virtual_objects = set()
        for file_name in file_list:
            virtual_object = VirtualObject(directory + "/" + file_name)
            virtual_objects.add(virtual_object)

        return virtual_objects
