#!/usr/bin/env python
#
# Copyright 2015-2018 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (absolute_import, division, print_function,
                        with_statement)

from firenado import session
from tornado import escape
from tornado import httputil
import tornado.wsgi
import os
import trac.web.main
import pexpect


def application(environ, start_response, component, handler, request):
    trac_root = component.conf['trac']['root']
    project_relative = "/".join(request.uri.split("/")[1:3])
    project_path = os.path.join(trac_root, project_relative)
    os.environ['TRAC_ENV'] = project_path
    environ['PATH_INFO'] = environ['PATH_INFO'].replace("/%s" %
                                                        project_relative, "")
    print(project_relative)

    if component.project_exists(project_relative):
        command = "trac-admin %s  config get header_logo src" % (project_path)
        print(command)
        child = pexpect.spawn(command)
        child.expect(pexpect.EOF)
        print(child.before)


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
    else:
        status = "404 Not Found"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        return ["File not found"]


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

        start_line = httputil.ResponseStartLine("HTTP/1.1", status_code,
                                                reason)
        header_obj = httputil.HTTPHeaders()
        for key, value in headers:
            header_obj.add(key, value)
        request.connection.write_headers(start_line, header_obj, chunk=body)
        request.connection.finish()
        self._log(status_code, request)
