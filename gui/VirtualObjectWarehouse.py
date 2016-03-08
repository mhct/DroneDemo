import os
from VirtualObject import VirtualObject


class VirtualObjectWarehouse:
    """
    The warehouse storing all virtual object
    """

    def __init__(self, directory, prefix):
        self._all_objects = set()
        self._added_objects = set()
        self._scan_objects(directory, prefix)

    def _scan_objects(self, directory, prefix):
        """
        Scan all input files whose names starting with the given prefix, create virtual object from those files and
        store them in a set.
        :param directory: the directory to be scanned
        :type directory: str
        :param prefix: the prefix
        :type prefix: str
        :return: a dictionary where keys are file names and values are the created virtual objects
        :rtype: dict
        """
        file_list = [f for f in os.walk(directory).next()[2] if f.startswith(prefix)]

        for file_name in file_list:
            virtual_object = VirtualObject(directory + "/" + file_name)
            self._all_objects.add(virtual_object)

    def get_all_objects(self):
        return self._all_objects

    def get_added_objects(self):
        return self._added_objects

    def add_object(self, virtual_object):
        self._all_objects.add(virtual_object)

    def update_added_objects(self, added_objects):
        self._added_objects = set(added_objects)
        self._all_objects = self._all_objects.union(added_objects)

