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

from . import handlers
from . import wsgi
from firenado import tornadoweb
import os


class NutracComponent(tornadoweb.TornadoComponent):

    def get_handlers(self):
        container = wsgi.ComponentizedWSGIContainer(wsgi.application, self)
        return [
            (r"/", handlers.IndexHandler),
            (r"/profile", handlers.ProfileHandler),
            (r"/login", handlers.ProfileHandler),
            (r"/([\w|\-|\_|\@|]*\/?)", handlers.HomeHandler),
            (r"/([\w|\-|\_|\@|]*)/.*", wsgi.ComponentizedFallbackHandler,
             dict(component=self, fallback=container))
        ]

    def get_config_filename(self):
        return "nutrac"

    def project_exists(self, trac_relative):
        trac_path = os.path.join(self.conf['trac']['root'], trac_relative)
        if os.path.exists(trac_path):
            return True
        return False
