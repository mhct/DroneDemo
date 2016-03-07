from VirtualObject import VirtualObject
from HttpDroneInterface import HttpDroneInterface


class MapSetter:
    def __init__(self, http_client):
        """
        :param http_client: the http client
        :type http_client: HttpDroneInterface
        """
        self._http_client = http_client

    def set_map(self, new_object_ids):
        """
        Add all objects that have ids in the object_id_list to the drone's virtual environment, remove all objects
        currently in the drone's virtual environment but not in the object_id_list
        :param new_object_ids: the list of the ids of objects
        :type new_object_ids: list of int
        """
        existing_object_ids = self._http_client.get_existing_object_ids()

        to_be_added_objects = self._get_to_be_added_objects(existing_object_ids, new_object_ids)
        to_be_removed_objects = self._get_to_be_removed_objects(existing_object_ids, new_object_ids)

        self._add_objects(to_be_added_objects)
        self._remove_objects(to_be_removed_objects)

    def _get_to_be_removed_objects(self, existing_object_ids, new_object_ids):
        to_be_removed_object = []

        for object_id in existing_object_ids:
            if object_id not in new_object_ids:
                virtual_object = VirtualObject("../virtualobjects/main_object" + str(object_id) + ".txt")
                to_be_removed_object.append(virtual_object)

        return to_be_removed_object

    def _get_to_be_added_objects(self, existing_object_ids, new_object_ids):
        to_be_added_object = []

        for object_id in new_object_ids:
            if object_id not in existing_object_ids:
                virtual_object = VirtualObject("../virtualobjects/main_object" + str(object_id) + ".txt")
                to_be_added_object.append(virtual_object)

        return to_be_added_object

    def _add_objects(self, to_be_added_objects):
        for virtual_object in to_be_added_objects:
            self._http_client.add_virtual_object(virtual_object)

    def _remove_objects(self, to_be_removed_objects):
        for virtual_object in to_be_removed_objects:
            self._http_client.remove_virtual_object(virtual_object)
