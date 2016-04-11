import HttpServer
import json

class TestHttpServer:

    def setup_method(self, method):
        self.app = HttpServer.app
        self.app.config['TESTING'] = True
        server_name = "127.0.0.1:7000"
        self.URL = "http://" + server_name
        self.app.config['SERVER_NAME'] = server_name
        # self.app.run()
        self.empty_virtual_environment = { "environment_configuration": [
            [
                50,
                50
            ],
            [
                100,
                100
            ]
        ],
            "virtual_objects": []
        }


    def test_app_is_running(self):
        client = self.app.test_client()

        assert client.get(self.URL + "/").status_code == 200


    def test_get_virtual_environment(self):
        expected_response = self.empty_virtual_environment
        client = self.app.test_client()

        response = client.get(self.URL + "/virtualEnvironment")
        assert response.status_code == 200
        assert json.loads(response.get_data()) == expected_response


    def test_add_virtual_object_bad(self):
        client = self.app.test_client()
        response = client.post(self.URL + "/virtualEnvironment")

        assert response.status_code == 400


    def test_add_virtual_object_ok_and_duplicate(self):
        client = self.app.test_client()
        virtual_object_json = json.dumps({"cells":[[2,2,33],[22,22,23]]})

        response = client.post(self.URL + "/virtualEnvironment", data=virtual_object_json)
        assert response.status_code == 200

        response = client.post(self.URL + "/virtualEnvironment", data=virtual_object_json)
        assert response.status_code == 409

    def test_delete_virtual_object_from_client_bad(self):
        client = self.app.test_client()
        data = dict()
        data["cells"] = list([[12, 33, 333]])

        json_data = json.dumps(data)

        #raw_json = "{\"cells\": [[12, 33, 333], [12, 34, 333]]}"
                     # {"cells":[[12,33,333],[12,34,333]]}
        response = client.delete(self.URL + "/virtualEnvironment", data=json_data)
        assert response.status_code == 200


    def test_delete_virtual_object_bad_request(self):
        client = self.app.test_client()
        response = client.delete(self.URL + "/virtualEnvironment")

        assert response.status_code == 400


    def test_delete_virtual_object(self):
        client = self.app.test_client()
        virtual_object_json = json.dumps({"cells":[[5,5,50]]})

        client.post(self.URL + "/virtualEnvironment", data=virtual_object_json)

        response = client.delete(self.URL + "/virtualEnvironment", data=virtual_object_json)
        assert response.status_code == 200

        response = client.delete(self.URL + "/virtualEnvironment", data=virtual_object_json)
        assert response.status_code == 409


    def test_get_virtual_environment_with_objects(self):
        HttpServer._virtual_environment.clear_map()

        vo1 = {"cells":[[3,3,33]]}
        vo2 = {"cells":[[7,7,71], [7,8,81]]}
        expected_virtual_objects = [vo2, vo1]

        client = self.app.test_client()
        client.post(self.URL + "/virtualEnvironment", data=json.dumps(vo1))
        client.post(self.URL + "/virtualEnvironment", data=json.dumps(vo2))

        response = client.get(self.URL + "/virtualEnvironment")

        assert response.status_code == 200

        response_data = json.loads(response.get_data())
        assert len(response_data['virtual_objects']) == 2
        assert vo1 in response_data['virtual_objects']
        assert vo2 in response_data['virtual_objects']


