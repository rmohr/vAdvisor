from prometheus_client import REGISTRY
from prometheus import LibvirtCollector, make_wsgi_app
from wsgiref.simple_server import make_server

from rest import make_rest_app


def assemble_app():
    prom_app = make_wsgi_app()
    rest_app = make_rest_app()

    def app(environ, start_response):
        path = environ.get('PATH_INFO', '').lstrip('/')
        if path == 'metrics':
            return prom_app(environ, start_response)
        else:
            return rest_app(environ, start_response)
    return app


def run():
    REGISTRY.register(LibvirtCollector())
    httpd = make_server('', 8181, assemble_app())
    httpd.serve_forever()

if __name__ == '__main__':
    run()