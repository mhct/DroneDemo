from PyQt4 import QtGui

from HttpClient import HttpClient

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_widget = QtGui.QListWidget()
        self.button = QtGui.QPushButton("Start")
        self.button.clicked.connect(self._start_http_client)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.threads = []

    def _start_http_client(self):
        http_client = HttpClient()
        http_client.map_signal.connect(self._write_to_screen)
        self.threads.append(http_client)
        http_client.start()

    def _write_to_screen(self, elevation_map):
        map_str = ""

        for x in range(len(elevation_map)):
            for y in range(len(elevation_map[0])):
                map_str += str(elevation_map[x][y])
            map_str += "\n"
        map_str += "\n"

        self.list_widget.addItem(unicode(map_str))
