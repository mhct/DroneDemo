import sys
from PyQt4 import QtGui

from gui.Controller import Controller
from gui.HttpDroneInterface import HttpDroneInterface
from gui.View import View
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse


class DroneApp:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        # initialize the client
        drone_interface = HttpDroneInterface()
        # initialize the virtual object warehouse
        warehouse = VirtualObjectWarehouse("../virtualobjects", "virtual_object")
        controller = Controller(drone_interface, warehouse)
        self._view = View(controller)

        sys.exit(app.exec_())


if __name__ == "__main__":
    app = DroneApp()
