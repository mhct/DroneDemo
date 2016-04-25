import json
from abc import ABCMeta

import requests
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtWrapperType
from VirtualEnvViewer.Helper import MapParams, Resolution, MapWidth, Cell
from VirtualEnvViewer.VirtualObject import VirtualObject


class FinalMeta(ABCMeta, pyqtWrapperType):
    pass


class VirtualEnvironmentService(QObject):
    __metaclass__ = FinalMeta

    # virtual_env_update_signal = QtCore.pyqtSignal(object, object)

    def __init__(self, virtual_env_url):
        QObject.__init__(self)
        self.virtual_env_url = virtual_env_url

    def get_elevation_map(self):
        r = requests.get(self.virtual_env_url + "/virtualEnvironment")

        data = json.loads(r.text)
        return self._parse_elevation_map_data(data)

    def _parse_elevation_map_data(self, data):

        env_configuration_raw = data['environment_configuration']
        resolution_data = env_configuration_raw[0]
        width_data = env_configuration_raw[1]

        map_params = MapParams(Resolution(resolution_data[0], resolution_data[1]),
                               MapWidth(width_data[0], width_data[1]))

        virtual_objects_data = data['virtual_objects']
        virtual_objects = []
        for i in virtual_objects_data:
            temp = set()
            for cell in i['cells']:
                temp.add(Cell(int(cell[0]), int(cell[1]), int(cell[2])))
            virtual_objects.append(VirtualObject(cells=frozenset(temp)))

        print virtual_objects
        return (map_params, set(virtual_objects))

    def send_update_command(self, to_be_added_objects, to_be_removed_objects):
        for obj in to_be_added_objects:
            self._add_virtual_object(obj)

        for obj in to_be_removed_objects:
            self._delete_virtual_object(obj)

    def reset_pose(self):
        r = requests.post(self.virtual_env_url + "/virtualEnvironment/reset")

        if r.status_code == 200:
            return True
        else:
            return False

    def _add_virtual_object(self, virtual_object):
        # data = {"cells": list(virtual_object.get_cells())}
        data = dict()
        data["cells"] = list(virtual_object.get_cells())
        print json.dumps(data)
        bla = json.dumps(data)

        r = requests.post(self.virtual_env_url + "/virtualEnvironment", json=json.dumps(data))

        return True  # FIXME

    def _delete_virtual_object(self, virtual_object):
        # data = {"cells": list(virtual_object.get_cells())}

        data = dict()
        data["cells"] = list(virtual_object.get_cells())
        print json.dumps(data)
        bla = json.dumps(data)

        r = requests.delete(self.virtual_env_url + "/virtualEnvironment", json=json.dumps(data))
        return True  # FIXME
