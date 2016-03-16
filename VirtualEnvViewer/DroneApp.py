import sys
from PyQt4 import QtGui

from VirtualEnvViewer.gui import Controller
from gui.VirtualEnvironmentService import VirtualEnvironmentService
from gui.View import View
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse, LocalLoaderVirtualObjects
import gui.HttpServer

class DroneApp:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        # creates the webserver to receive drone poses
        webapp = gui.HttpServer.webapp
        webapp.start()

        # initialize the client
        virtual_environment_service = VirtualEnvironmentService()
        # initialize the virtual object warehouse
        local_virtual_objects = LocalLoaderVirtualObjects.load_virtual_objects("../resources_virtualobjects", "virtual_object")

        warehouse = VirtualObjectWarehouse()
        warehouse.add_outside_virtual_environment_objects(local_virtual_objects)

        controller = Controller(gui.HttpServer.qconn, virtual_environment_service, warehouse)
        self._view = View(controller)

        sys.exit(app.exec_())


if __name__ == "__main__":
    app = DroneApp()
