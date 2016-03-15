import flask
from flask import jsonify, request, Response

from VirtualEnvironment import VirtualEnvironment
from Helper import MapWidth, CellSize, MapParams
from VirtualObject import VirtualObject




__author__ = 'mario'


app = flask.Flask(__name__)
_virtual_environment = VirtualEnvironment(MapParams(MapWidth(50,50), CellSize(100,100)))

@app.route("/")
def root():
    return "Hello World!"

@app.route("/virtualEnvironment", methods=['GET'])
def get_virtual_environment():
    environment_configuration = _virtual_environment.get_map_params()
    a = _virtual_environment.get_virtual_objects()

    return jsonify(environment_configuration=environment_configuration, virtual_objects=a)


@app.route("/virtualEnvironment", methods=['POST'])
def add_object():
    data = request.get_json(force=True)
    if data:
        virtual_object_data = data["cells"]
        if data['cells']:
            vo = VirtualObject(virtual_object_data)
            try:
                _virtual_environment.add_virtual_object(vo)
            except ValueError as e:
                return Response(response=e, status=409)

            return Response(status=200)

    else:
        return Response(status=400)

@app.route("/virtualEnvironment", methods=['DELETE'])
def delete_object():
    data = request.get_json(force=True)
    if data:
        virtual_object_data = data["cells"]
        if data['cells']:
            vo = VirtualObject(virtual_object_data)
            if _virtual_environment.remove_virtual_object(vo):
                return Response(status=200)
            else:
                return Response(response="Virtual Object Not found.", status=409)



    else:
        return Response(status=400)
