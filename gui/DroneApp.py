import sys
from PyQt4 import QtGui

from gui.Controller import Controller


class DroneApp:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        controller = Controller()
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = DroneApp()
