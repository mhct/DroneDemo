from PyQt4 import QtCore

from Environment import Environment


class HttpClient(QtCore.QThread):

    map_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self._env = Environment(4, 4, 1, 1)
        print "test"

    def run(self):
        for i in range(10):
            self.map_signal.emit(self._env.get_elevation_map())
            self.sleep(2)