from PyQt4 import QtCore
from PyQt4.QtCore import QThread, QObject
import flask
from flask import jsonify, request, Response

_app = flask.Flask(__name__)

class QConnector(QObject):
    drone_pose_update_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)

    def emit(self, data):
        self.drone_pose_update_signal.emit(data)


qconn = QConnector()

@_app.route("/")
def root():
    return "Send me your location."


@_app.route("/drones/1/locations", methods=['POST'])
def add_object():
    data = request.get_json(force=True)
    if data:
        # qconn.emit(data)
        if 'Point' == data['type'] and isinstance(data['coordinates'], list) and len(data['coordinates']) == 3:
            qconn.emit(data['coordinates'])
            return Response(status=200)
        else:
            return Response(status=400)

    else:
        return Response(status=400)


class MyApp(QThread):

    def __init__(self, myApp):
        QThread.__init__(self)

        self.app = myApp

    def run(self):
        self.app.run()


webapp = MyApp(_app)