from Server import HttpServer

app = HttpServer.app
app.config['TESTING'] = False
server_name = "127.0.0.1:7000"
URL = "http://" + server_name
app.config['SERVER_NAME'] = server_name