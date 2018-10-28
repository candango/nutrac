#!/usr/bin/env python
#
# Copyright 2018 Flavio Garcia
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

from . import forms
from firenado import tornadoweb
from tornado import escape


class IndexHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.render("index.html")


class ProfileHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("Profile output")


class LoginHandler(tornadoweb.TornadoHandler):

    def get(self, repository_path=None):
        self.render("login.html")

    def post(self):
        error_data = {'errors': {}}
        request_data = escape.json_decode(self.request.body)
        form = forms.SigninForm(request_data, handler=self)
        if form.validate():
            pass
        else:
            self.set_status(403)
            error_data['errors'].update(form.errors)
            self.write(error_data)


class HomeHandler(tornadoweb.TornadoHandler):

    def get(self, user):
        self.write("Home output %s" % user)
