import flask
from flask import jsonify, request, Response
from jsonpickle import json

from Configuration import Configuration
from VirtualEnvironment import VirtualEnvironment
from VirtualObject import VirtualObject




__author__ = 'mario'


app = flask.Flask(__name__)
configuration = Configuration()
_virtual_environment = VirtualEnvironment(configuration.get_map_params())
need_reset_pose = False


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
        processed_data = json.loads(data)
        virtual_object_data = processed_data["cells"]
        virtual_object_name = processed_data["name"]
        if virtual_object_data:
            vo = VirtualObject(virtual_object_data, virtual_object_name)
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
        processed_data = json.loads(data)
        virtual_object_data = processed_data["cells"]
        virtual_object_name = processed_data["name"]
        if virtual_object_data:
            vo = VirtualObject(virtual_object_data, virtual_object_name)
            if _virtual_environment.remove_virtual_object(vo):
                return Response(status=200)
            else:
                return Response(response="Virtual Object Not found.", status=409)



    else:
        return Response(status=400)

@app.route("/virtualEnvironment/reset", methods=['POST'])
def reset_pose():
    print "reset"
    if get_reset_pose():
        return Response(status=200)
    else:
        return Response(status=409)


def set_reset_pose():
    need_reset_pose = True

def get_reset_pose():
    return need_reset_pose


print "AAA"
app.run(port=7000)