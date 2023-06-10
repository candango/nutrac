# Copyright 2018-2023 Flavio Garcia
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

from .services import ProjectService
from firenado.service import with_service
from firenado.tornadoweb import TornadoHandler
import os
import pexpect
import logging

logger = logging.getLogger(__name__)


class TracdHandler:

    @property
    def trac_root(self):
        return self.component.conf['trac']['root']

    def path_exists(self, path):
        return os.path.exists(self.trac_rooted(path))

    def trac_rooted(self, path):
        return os.path.join(self.trac_root, path)


class IndexHandler(TornadoHandler):

    def get(self):
        self.render("index.html")


class ProfileHandler(TornadoHandler):

    def get(self):
        self.write("Profile output")


class HomeHandler(TornadoHandler, TracdHandler):

    @with_service(ProjectService)
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


class UpgradeHandler(TornadoHandler, TracdHandler):

    project_service: ProjectService

    @with_service(ProjectService)
    def get(self, repository_path=None):
        real_repository_path = self.trac_rooted(repository_path)
        upgrade_cmd = "trac-admin %s upgrade"
        wiki_upgrade_cmd = "trac-admin %s wiki upgrade"
        logger.warn("Upgrading repository %s" % repository_path)
        if self.path_exists(real_repository_path):
            try:
                child = pexpect.spawn(upgrade_cmd % real_repository_path)
                child.expect(pexpect.EOF)
            except pexpect.ExceptionPexpect as ep:
                self.write(str(ep))
                self.render("nutrac:upgrade.html")
            else:
                if "Error" in child.before:
                    self.write(child.before)
                    self.render("nutrac:upgrade.html")
                else:
                    logger.warn("Repository %s was upgraded." %
                                repository_path)
                    logger.warn("Upgrading repository %s wiki." %
                                repository_path)
                    # TODO: handle wiki upgrade exception
                    child = pexpect.spawn(wiki_upgrade_cmd %
                                          real_repository_path)
                    child.expect(pexpect.EOF)
                    logger.warn("Repository %s wiki was upgraded." %
                                repository_path)
                    self.redirect("/%s" % repository_path)
