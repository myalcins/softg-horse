from core.tcp_server import TCPServer
from utils.utils import http_to_environ, to_environ, wsgi_to_bytes, parser
from datetime import datetime
from wsgi import app   


class WSGIServer:

    response_header = []
    client = None

    def __init__(self, address, application):
        self.server = TCPServer
        self.host = address.split(":")[0]
        self.port = address.split(":")[1]
        self.application = application

    def run(self):
        self.server = self.server(self.request_handle)
        self.server.serve()

    def request_handle(self, client):
        self.client = client
        request = self.client.recv(1024).decode()
        env = http_to_environ(request, to_environ)
        response = self.application(env, self.start_response)
        self.complete_request(response)

    def complete_request(self, responses):
        res = self.create_response()
        for response in responses:
            res += response
        try:
            self.client.sendall(res)
        finally:
            self.client.close()

    def create_response(self):
        status, headers = self.response_header
        res = wsgi_to_bytes("HTTP/1.1 %s\r\n" % status)
        for header in headers:
            res += wsgi_to_bytes('{0}: {1}\r\n'.format(*header))
        res += wsgi_to_bytes("Date: %s\r\n" % str(datetime.now()))
        res += wsgi_to_bytes("Server: %s\r\n" % "soft-ghorse")
        res += wsgi_to_bytes("\r\n")
        return res
        
    def start_response(self, status, headers):
        self.response_header = [status, headers]


serv = WSGIServer("localhost:8000" ,app)
serv.run()









