from gui import VirtualEnvironmentService


class MapSetter:
    def __init__(self, drone_interface):
        """
        :param drone_interface: the drone interface
        :type drone_interface: VirtualEnvironmentService
        """
        self._drone_interface = drone_interface

    def set_map(self, selected_virtual_objects, existing_virtual_objects):
        """
        Add all objects in the file list to the drone's virtual environment, remove all objects currently in the
        drone's virtual environment but not in the file list.
        :param selected_virtual_objects: the list of the files that contain to be added objects
        :type selected_virtual_objects: list of str
        """
        to_be_added_objects = self._get_to_be_added_objects(existing_virtual_objects, selected_virtual_objects)
        to_be_removed_objects = self._get_to_be_removed_objects(existing_virtual_objects, selected_virtual_objects)

        self._drone_interface.send_update_command(to_be_added_objects, to_be_removed_objects)

    def _get_to_be_removed_objects(self, existing_objects, selected_objects):
        to_be_removed_objects = []

        for virtual_object in existing_objects:
            if virtual_object not in selected_objects:
                to_be_removed_objects.append(virtual_object)

        return to_be_removed_objects

    def _get_to_be_added_objects(self, existing_objects, selected_objects):
        to_be_added_objects = []

        for virtual_object in selected_objects:
            if virtual_object not in existing_objects:
                to_be_added_objects.append(virtual_object)

        return to_be_added_objects
