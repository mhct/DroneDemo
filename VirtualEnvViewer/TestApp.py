import sys
from PyQt4 import QtGui
import gui.HttpServer

class DroneApp:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        webapp = gui.HttpServer.webapp
        webapp.start()

        sys.exit(app.exec_())

if __name__ == "__main__":
    app = DroneApp()
