from abc import ABCMeta
from PyQt4 import QtCore

from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtWrapperType
import requests
import json

class FinalMeta(ABCMeta, pyqtWrapperType):
    pass


class VirtualEnvironmentService(QObject):
    __metaclass__ = FinalMeta

    drone_pose_update_signal = QtCore.pyqtSignal(object)
    virtual_env_update_signal = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super(self)
        # self._env = VirtualEnvironment(MapWidth(50, 50), Resolution(100, 100))

    def __init__(self, virtual_env_url):
        self.virtual_env_url = virtual_env_url

    def get_elevation_map(self):
        r = requests.get(self.virtual_env_url + "/virtualEnvironment")

        data = json.loads(r.text)
        env_configuration = data['environment_configuration']
        virtual_objects = data['virtual_objects']

        return (env_configuration, virtual_objects)

    def add_virtual_object(self, virtual_object):
        data = {'cells': virtual_object.get_cells()}
        r = requests.post(self.virtual_env_url + "/virtualEnvironment", json=json.dumps(data))

        return True #FIXME

    def delete_virtual_object(self, virtual_object):
        data = {'cells': virtual_object.get_cells()}
        r = requests.delete(self.virtual_env_url + "/virtualEnvironment", json=json.dumps(data))
        return True #FIXME

    # def get_drone_pose(self):
    #     return self._server.get_drone_pose()
    #
    # def update_drone_pose(self, drone_pose):
    #     self.drone_pose_update_signal.emit(drone_pose)
