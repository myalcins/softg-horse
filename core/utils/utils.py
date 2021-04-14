import os, sys, io
from socket import error


enc, esc = sys.getfilesystemencoding(), 'surrogateescape'


def unicode_to_wsgi(u):
    # Convert an environment variable to a WSGI "bytes-as-unicode" string
    return u.encode(enc, esc).decode('iso-8859-1')


def wsgi_to_bytes(s):
    return s.encode()


def parser(http):
    request, *headers, _, body = http.split('\r\n')
    method, path, protocol = request.split(' ')
    headers = dict(
            line.split(':', maxsplit=1) for line in headers
        )
    return method, path, protocol, headers, body


def http_to_environ(http, to_environ):
    request = parser(http)
    env = to_environ(*request)
    return env


def to_environ(*request):
    env = default_env()
    env["wsgi.url_scheme"] = "http"
    env['REQUEST_METHOD'] = request[0]
    env['SERVER_NAME'] = "localhost"
    env['PATH_INFO'] = request[1]
    env['SERVER_PORT'] = "8080"
    env['SERVER_PROTOCOL'] = request[2]
    if request[4]:
        env['wsgi.input'] = io.StringIO(request[4])
    return env


def default_env():
    return {
        "wsgi.version": (1,0),
        "wsgi.errors": sys.stderr,
        "wsgi.run_once": True,
        "wsgi.multithread": True,
        "wsgi.multiprocess": False,
    }


def start_response(status, headers):
    response_header = [status, headers]
    return response_header