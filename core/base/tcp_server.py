from socket import socket,  AF_INET, SOCK_STREAM, error
from .base_socket import BaseSocket
from threading import Thread


class TCPServer(BaseSocket):
    host = "localhost"
    port = 8080
    
    def __init__(self, RequestHandler):
        self.__addr_family = AF_INET
        self.__socket_type = SOCK_STREAM
        self.request_queue_size = 1024
        self.RequestHandler = RequestHandler

    def configure_server(self):
        try:
            self.socket.bind((self.host, self.port))
        except:
            print("server configuration error.")

    def start_server(self):
        self.start_socket()
        try:
            self.configure_server()
        except:
            print("server running error.")

    def serve(self):
        try:
            self.start_server()
            print(f"http://{self.host}:{self.port} listening....")
            self.socket.listen(self.request_queue_size)
            while True:
                try:
                    client, address = self.socket.accept()
                    print(f"Connected at {address}")
                    Thread(target=self.RequestHandler, args=(client,), daemon=False).start()
                except:
                    self.socket.close()
        except KeyboardInterrupt as key:
                self.socket.close()
                print("Quit the server with keyboard interrupt.")
                exit(1)
        except:
            print("server serving error.")
        
