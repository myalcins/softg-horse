from core import server
import sys, importlib


def get_app():
    app = importlib.import_module(sys.argv[2].split(':')[0])
    app = app.__getattribute__(sys.argv[2].split(':')[1])
    return app

if __name__ == '__main__':
    wsgi_server = server.WSGIServer(sys.argv[1], get_app())
    wsgi_server.run()
