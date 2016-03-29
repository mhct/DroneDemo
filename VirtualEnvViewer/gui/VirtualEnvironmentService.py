import json
from abc import ABCMeta

import requests
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtWrapperType


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
