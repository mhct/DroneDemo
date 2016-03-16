from PyQt4 import QtCore


class VirtualEnvironmentGetter(QtCore.QThread):
    map_signal = QtCore.pyqtSignal(object, object)

    def __init__(self, virtual_environment_service):
        """
        :param http_client: the http client instance
        :type http_client: HttpClient
        :return:
        :rtype:
        """
        QtCore.QThread.__init__(self)
        self._virtual_environment_service = virtual_environment_service

    def run(self):
        """
        Update map for each second
        """
        while True:
            self.sleep(1)  # in seconds
            (env_configuration, virtual_objects) = self._virtual_environment_service.get_elevation_map()
            self.map_signal.emit(env_configuration, virtual_objects)
