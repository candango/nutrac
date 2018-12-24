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

from __future__ import (absolute_import, division, print_function,
                        with_statement)

from . import handlers
from . import wsgi
from firenado import tornadoweb
from firenado.config import get_class_from_name
import logging
import os
import sys

logger = logging.getLogger(__name__)


class NutracComponent(tornadoweb.TornadoComponent):

    def __init__(self, name, application):
        super(NutracComponent, self).__init__(name, application)
        self.auth_config = None
        self.wsgi_application = wsgi.NutracWsgiApplication(self)
        self.id = None

    def get_handlers(self):
        if "id" not in self.conf or self.conf['id'] is None:
            #TODO: point to the complete file name here
            logger.fatal("Nutrac instance without an id set. The id must be "
                         "defined at the %s config file." %
                         self.get_config_filename())
            sys.exit(1)
        else:
            self.id = self.conf['id']
            logger.info("Nutrac instance id is %s." % self.id)

        container = wsgi.ContextualizedWSGIContainer(
            self.wsgi_application.process
        )
        self.auth_config = get_class_from_name(
            self.conf['auth']['config']
        )()
        return [
            (r"/", handlers.IndexHandler),
            (r"/profile", handlers.ProfileHandler),
            (r"/login", self.auth_config.get_login_handler()),
            (r"/([\w|\-|\_|\@|]*\/?)", handlers.HomeHandler),
            (r"/([\w|\-|\_|\@|]*/[\w|\-|\_|\@|]*)/login",
             self.auth_config.get_login_handler()),
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
