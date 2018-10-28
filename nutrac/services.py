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

from .models import UserBase
import bcrypt
from firenado import service


class LoginService(service.FirenadoService):

    @service.served_by("nutrac.services.UserService")
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


class UserService(service.FirenadoService):

    def by_username(self, username):
        db_session = self.get_data_source("nutrac").session
        user = db_session.query(UserBase).filter(
            UserBase.username == username.lower()).one_or_none()
        db_session.close()
        return user
