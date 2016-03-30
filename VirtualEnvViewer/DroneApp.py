import sys

from PyQt4 import QtGui
from VirtualEnvViewer.gui.MockVirtualEnvironmentService import MockVirtualEnvironmentService

import gui.HttpServer
from VirtualEnvViewer.gui import Controller
from gui.View import View
from gui.VirtualEnvironmentService import VirtualEnvironmentService
from gui.VirtualObjectWarehouse import VirtualObjectWarehouse, LocalLoaderVirtualObjects
from gui.Controller import Controller


class DroneApp:
    server_url = "http://127.0.0.1:7000"

    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        # creates the webserver to receive drone poses
        webapp = gui.HttpServer.webapp
        webapp.start()

        # initialize the client
        virtual_environment_service = VirtualEnvironmentService(self.server_url)
        # virtual_environment_service = MockVirtualEnvironmentService(self.server_url)
        # initialize the virtual object warehouse
        local_virtual_objects = LocalLoaderVirtualObjects.load_virtual_objects("resources_virtualobjects", "virtual_object")

        warehouse = VirtualObjectWarehouse()
        for virtual_object in local_virtual_objects:
            warehouse.add_outside_virtual_environment_objects(virtual_object)

        controller = Controller(gui.HttpServer.qconn, virtual_environment_service, warehouse)
        self._view = View(controller)

        sys.exit(app.exec_())


if __name__ == "__main__":
    app = DroneApp()
