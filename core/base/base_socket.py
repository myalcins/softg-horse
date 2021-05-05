from os import error
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from sys import stderr


class BaseSocket(object):

    def __init__(self):
        self.socket = None

    def create_socket(self):
        try:
            self.socket = socket(self.__addr_family, self.__socket_type)
        except:
            print("socket creating error.")

    def close_socket(self):
        if self.socket:
            self.socket.close()

    def conf_socket(self):
        try:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except OSError as e:
            print("socket configuration error.")
        
    def start_socket(self):
        try:
            self.create_socket()
            self.conf_socket()
        except:
            print("socket couldn't start..")
