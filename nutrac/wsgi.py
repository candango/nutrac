#!/usr/bin/env python
#
# Copyright 2018-2019 Flavio Garcia
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

from firenado import service, session
from firenado.data import DataConnectedMixin
from tornado import escape, httputil
import tornado.wsgi
import os
import trac.web.main
import pexpect
from nutrac import services


class NutracWsgiApplication(DataConnectedMixin):

    repository_service = None  # type: services.ProjectService
    user_service = None  # type: services.UserService

    def __init__(self, component):
        self.repository_service = None
        self.user_service = None
        self.component = component
        self.data_connected = self.component.application

    @service.served_by(services.ProjectService)
    @service.served_by(services.UserService)
    def process(self, environ, start_response, handler, request):
        """ Process the user state and environment variables necessary to
        dispatch the request correctly to the trac instance being requested.

        :param environ: Environment variables to be sent to the trac
        :param start_response:
        :param ComponentizedFallbackHandler handler: The
        ComponentizedFallbackHandler triggering the process method
        :param request: The real Tornado request
        :return: The dispatched request returned from trac
        """
        #user = self.user_service.by_username("nutracmin")
        user = None
        trac_root = self.component.conf['trac']['root']
        project_relative = "/".join(request.uri.split("/")[1:3])
        project_path = os.path.join(trac_root, project_relative, "trac")
        os.environ['TRAC_ENV'] = project_path
        environ['PATH_INFO'] = environ['PATH_INFO'].replace(
            "/%s" % project_relative, "")
        if user:
            environ['REMOTE_USER'] = user.username
        else:
            environ['REMOTE_USER'] = "anonymous"

        print(project_relative)

        if self.component.project_exists(project_relative):
            if user:
                if user.email:
                    command = "trac-admin %s session set email %s %s" % (
                        project_path, user.username, user.email)
                else:
                    command = "trac-admin %s session set email %s \"\" " % (
                        project_path, user.username)
                print(command)
                child = pexpect.spawn(command)
                child.expect(pexpect.EOF)
                print(child.before)

            environ['SCRIPT_NAME'] = "/%s/" % project_relative

            request.application = self.component.application
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


class ContextualizedWSGIContainer(tornado.wsgi.WSGIContainer):

    def __init__(self, wsgi_application):
        super(ContextualizedWSGIContainer, self).__init__(wsgi_application)
        self.handler = None

    def __call__(self, request):
        data = {}
        response = []

        def start_response(status, response_headers, exc_info=None):
            data["status"] = status
            data["headers"] = response_headers
            return response.append
        app_response = self.wsgi_application(
            ContextualizedWSGIContainer.environ(request), start_response,
            self.handler, request)
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
