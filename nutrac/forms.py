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

from .services import LoginService
from firenado.service import with_service
from wtforms import ValidationError
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from tornado_wtforms import TornadoForm

FORM_PASSWORD_MISSING = "Password missing."
FORM_USERNAME_MISSING = "User name missing."
FORM_INVALID_USERNAME_OR_PASSWORD = "Invalid user name or password."


class SigninForm(TornadoForm):

    login_service = None  # type: nutrac.services.LoginService
    password = PasswordField(validators=[DataRequired(FORM_PASSWORD_MISSING)])
    username = StringField(validators=[DataRequired(FORM_USERNAME_MISSING)])
    form = StringField()

    def __init__(self, formdata=None, obj=None, prefix='', locale_code='en_US',
                 handler=None,
                 **kwargs):
        super(SigninForm, self).__init__(formdata, obj, prefix, **kwargs)
        self.handler = handler
        self.login_service = None

    @with_service(LoginService)
    def validate_form(self, field):
        if self.username.data and self.password.data:
            if not self.login_service.is_valid(self.username.data.lower(),
                                               self.password.data):
                raise ValidationError(FORM_INVALID_USERNAME_OR_PASSWORD)

    def get_data_connected(self):
        if self.handler:
            return self.handler.application
        return None
