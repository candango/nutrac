from . import handlers
from firenado import tornadoweb, session
import tornado.web

import base64
import os
import sys

import logging
import logging.handlers

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.wsgi
from tornado import escape
from tornado import httputil

import trac.web.main


def application(environ, start_response, component, handler, request):
    trac_root = component.conf['trac']['root']
    project_relative = "/".join(request.uri.split("/")[1:3])
    project_path = os.path.join(trac_root, project_relative)
    os.environ['TRAC_ENV'] = project_path
    environ['PATH_INFO'] = environ['PATH_INFO'].replace("/%s" %
                                                        project_relative, "")
    environ['SCRIPT_NAME'] = "/%s/" % project_relative
    environ['REMOTE_USER'] = "buga"

    request.application = component.application
    #environ['trac.env_path'] = os.path.join(PROJECT_ROOT, '..', '..')
    #environ['trac.base_path'] = 'candango'
    #if 'HTTP_AUTHORIZATION' in environ:
        #auth_header = environ['HTTP_AUTHORIZATION']
        #environ['REMOTE_USER'] = base64.decodestring(auth_header[6:]).split(':')[0]
    #environ['SCRIPT_NAME'] = os.path.join('/', sys.argv[1])
    return trac.web.main.dispatch_request(environ, start_response)




class ComponentizedWSGIContainer(tornado.wsgi.WSGIContainer):

    def __init__(self, wsgi_application, component):
        super(ComponentizedWSGIContainer, self).__init__(wsgi_application)
        self.component = component
        self.handler = None

    def __call__(self, request):
        data = {}
        response = []

        def start_response(status, response_headers, exc_info=None):
            data["status"] = status
            data["headers"] = response_headers
            return response.append
        app_response = self.wsgi_application(
            ComponentizedWSGIContainer.environ(request), start_response,
            self.component, self.handler, request)
        self.handler = None
        try:
            response.extend(app_response)
            body = b"".join(response)
        finally:
            if hasattr(app_response, "close"):
                app_response.close()
        if not data:
            raise Exception("WSGI app did not call start_response")

        status_code, reason = data["status"].split(' ', 1)
        status_code = int(status_code)
        headers = data["headers"]
        header_set = set(k.lower() for (k, v) in headers)
        body = escape.utf8(body)
        if status_code != 304:
            if "content-length" not in header_set:
                headers.append(("Content-Length", str(len(body))))
            if "content-type" not in header_set:
                headers.append(("Content-Type", "text/html; charset=UTF-8"))
        if "server" not in header_set:
            headers.append(("Server", "TornadoServer/%s" % tornado.version))

        start_line = httputil.ResponseStartLine("HTTP/1.1", status_code, reason)
        header_obj = httputil.HTTPHeaders()
        for key, value in headers:
            header_obj.add(key, value)
        request.connection.write_headers(start_line, header_obj, chunk=body)
        request.connection.finish()
        self._log(status_code, request)


class ComponentizedFallbackHandler(tornado.web.FallbackHandler):

    def initialize(self, component, fallback):
        self.component = component
        fallback.handler = self
        super(ComponentizedFallbackHandler, self).initialize(fallback)

    @session.read
    def prepare(self):
        super(ComponentizedFallbackHandler, self).prepare()

    @session.write
    def on_finish(self):
        pass
        # self.component.run_after_handler(self)


class IntracComponent(tornadoweb.TornadoComponent):

    def get_handlers(self):
        container = ComponentizedWSGIContainer(application, self)
        return [
            (r"/", handlers.IndexHandler),
            (r"/profile", handlers.ProfileHandler),
            (r"/([\w|\-|\_|\@|]*\/?)", handlers.ProjectsHandler),
            (r"/([\w|\-|\_|\@|]*)/.*", ComponentizedFallbackHandler,
             dict(component=self, fallback=container))
        ]

    def get_config_filename(self):
        return "intrac"
