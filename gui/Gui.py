import sys
from PyQt4 import QtGui

from MainWindow import MainWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
