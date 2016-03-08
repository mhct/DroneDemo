from VirtualObject import VirtualObject
from HttpDroneInterface import HttpDroneInterface


class MapSetter:
    def __init__(self, drone_interface, object_warehouse):
        """
        :param drone_interface: the drone interface
        :type drone_interface: HttpDroneInterface
        """
        self._drone_interface = drone_interface
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
        existing_object_hashcodes = self._drone_interface.get_existing_object_hashcodes()
        existing_object_file_names = self._get_file_names_by_hashcode(existing_object_hashcodes)

        to_be_added_object_file_names = self._get_to_be_added_object_file_names(existing_object_file_names,
                                                                                new_object_file_names)
        to_be_removed_object_hashcodes = self._get_to_be_removed_object_hashcodes(existing_object_file_names,
                                                                                  new_object_file_names)

        self._update_virtual_environment(to_be_added_object_file_names, to_be_removed_object_hashcodes)

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

    def _update_virtual_environment(self, to_be_added_object_file_names, to_be_removed_object_hashcodes):
        to_be_added_objects = self._get_list_object_by_file_names(to_be_added_object_file_names)
        added_object_hashcodes = self._drone_interface.send_update_command(to_be_added_objects,
                                                                           to_be_removed_object_hashcodes)

        self._update_hashcode(to_be_added_object_file_names, added_object_hashcodes)

    def _update_hashcode(self, to_be_added_object_file_names, added_object_hashcodes):
        if len(to_be_added_object_file_names) != len(added_object_hashcodes):
            raise ValueError("Inconsistent hashcodes.")

        for index in range(len(to_be_added_object_file_names)):
            self._object_warehouse.update_hashcode(to_be_added_object_file_names[index], added_object_hashcodes[index])

    def _get_file_names_by_hashcode(self, existing_object_hashcodes):
        file_names = []

        for hashcode in existing_object_hashcodes:
            file_names.append(self._object_warehouse.get_file_name_by_hashcode(hashcode))

        return file_names

    def _get_list_object_by_file_names(self, to_be_added_object_file_names):
        to_be_added_objects = []

        for file_name in to_be_added_object_file_names:
            to_be_added_objects.append(self._object_warehouse.get_virtual_object_by_filename(file_name))

        return to_be_added_objects
