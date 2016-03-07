from VirtualObject import VirtualObject
from HttpDroneInterface import HttpDroneInterface


class MapSetter:
    def __init__(self, http_client, object_warehouse):
        """
        :param http_client: the http client
        :type http_client: HttpDroneInterface
        """
        self._http_client = http_client
        self._object_warehouse = object_warehouse

    def set_map(self, new_object_file_names):
        """
        Add all objects in the file list to the drone's virtual environment, remove all objects currently in the
        drone's virtual environment but not in the file list.
        :param new_object_file_names: the list of the files that contain to be added objects
        :type new_object_file_names: list of str
        """
        # we get the object hashcodes again because it can be the case that another popup window is opened and update
        # the map of the drone before the current popup window update the map
        existing_object_hashcodes = self._http_client.get_existing_object_hashcodes()
        existing_object_file_names = self._get_file_names_by_hashcode(existing_object_hashcodes)

        to_be_added_objects_file_names = self._get_to_be_added_object_file_names(existing_object_file_names,
                                                                                 new_object_file_names)
        to_be_removed_object_hashcode = self._get_to_be_removed_object_hashcodes(existing_object_file_names,
                                                                                 new_object_file_names)

        self._add_objects(to_be_added_objects_file_names)
        self._remove_objects(to_be_removed_object_hashcode)

    def _get_to_be_removed_object_hashcodes(self, existing_object_file_names, new_object_file_names):
        to_be_removed_object_hashcodes = []

        for file_name in existing_object_file_names:
            if file_name not in new_object_file_names:
                to_be_removed_object_hashcodes.append(self._object_warehouse.get_hashcode_by_file_name(file_name))

        return to_be_removed_object_hashcodes

    def _get_to_be_added_object_file_names(self, existing_object_file_names, new_object_file_names):
        to_be_added_object_file_names = []

        for file_name in new_object_file_names:
            if file_name not in existing_object_file_names:
                to_be_added_object_file_names.append(file_name)

        return to_be_added_object_file_names

    def _add_objects(self, to_be_added_object_file_names):
        for file_name in to_be_added_object_file_names:
            hashcode = self._http_client.add_virtual_object(
                self._object_warehouse.get_virtual_object_by_filename(file_name))
            self._object_warehouse.update_hashcode(file_name, hashcode)

    def _remove_objects(self, to_be_removed_object_hashcodes):
        for hashcode in to_be_removed_object_hashcodes:
            self._http_client.remove_virtual_object(hashcode)

    def _get_file_names_by_hashcode(self, existing_object_hashcodes):
        file_names = []

        for hashcode in existing_object_hashcodes:
            file_names.append(self._object_warehouse.get_file_name_by_hashcode(hashcode))

        return file_names
