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

from . import services
from firenado import service, tornadoweb
import os


class TracdHandler:

    @property
    def trac_root(self):
        return self.component.conf['trac']['root']

    def path_exists(self, path):
        return os.path.exists(self.trac_rooted(path))

    def trac_rooted(self, path):
        return os.path.join(self.trac_root, path)


class IndexHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.render("index.html")


class ProfileHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("Profile output")


class HomeHandler(tornadoweb.TornadoHandler, TracdHandler):

    @service.served_by(services.ProjectService)
    def get(self, path):
        """
        :param basestring path:
        :return:
        """
        if self.path_exists(path):
            repos = self.project_service.get_projects(
                self.trac_rooted(path)
            )
            for repo in repos:
                self.write("%s</br>" % repo)
        else:
            self.set_status(404, "Path no found.")
