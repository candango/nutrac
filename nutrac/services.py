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

from .models import UserBase
import bcrypt
from firenado.service import FirenadoService, with_service
from firenado.sqlalchemy import with_session
from sqlalchemy import select
import os
from sqlalchemy.orm import Session


class ProjectService(FirenadoService):

    def get_projects(self, path):
        repos = []
        for dirname in os.listdir(path):
            if os.path.isdir(os.path.join(path, dirname)):
                repos.append(dirname)
        return repos

    def is_valid(self, path):
        return False


class LoginService(FirenadoService):

    user_service = None  # type: UserService

    def __init__(self, consumer, data_source=None):
        super(LoginService, self).__init__(consumer, data_source=None)
        self.user_service = None

    @with_service("nutrac.services.UserService")
    def is_valid(self, username, password):
        user = self.user_service.by_username(username)
        if user:
            if self.is_password_valid(password, user.password):
                return True
        return False

    def is_password_valid(self, challenge, encrypted_password):
        return bcrypt.checkpw(
            challenge.encode("utf-8"),
            encrypted_password.encode("utf-8")
        )


class UserService(FirenadoService):

    @with_session(data_source="nutrac")
    def by_username(self, username, **kwargs):
        session: Session = kwargs.get("session")
        stmt = select(UserBase).where(UserBase.username == username.lower())
        user = session.scalars(stmt).one_or_none()
        return user
