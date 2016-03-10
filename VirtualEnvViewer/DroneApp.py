import sys
from PyQt4 import QtGui

from VirtualEnvViewer.gui import Controller
from gui.VirtualEnvironmentService import VirtualEnvironmentService
from gui.View import View
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse


class DroneApp:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        # initialize the client
        drone_interface = VirtualEnvironmentService()
        # initialize the virtual object warehouse
        warehouse = VirtualObjectWarehouse("../resources_virtualobjects", "virtual_object")
        controller = Controller(drone_interface, warehouse)
        self._view = View(controller)

        sys.exit(app.exec_())


if __name__ == "__main__":
    app = DroneApp()
