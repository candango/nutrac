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

from ..models import UserBase
from ..security import generate_private_key
from passlib.hash import bcrypt
from firenado.management import ManagementTask
from firenado.util.sqlalchemy_util import Session, run_script
import logging
import os
from six import moves
from sqlalchemy import create_engine
import uuid


logger = logging.getLogger(__name__)


class NutacCreateDatabaseTask(ManagementTask):

    def add_arguments(self, parser):
        parser.add_argument("-d", "--database", default="nutrac")
        parser.add_argument("-H", "--host", default="localhost")
        parser.add_argument("-p", "--password")
        parser.add_argument("-P", "--port", default=5432, type=int)
        parser.add_argument("-u", "--user", default="nutrac")

    def run(self, namespace):
        """ Create the database
        """
        password = None
        if namespace.password is None:
            password = moves.input("Inform the database password:")
        else:
            password = namespace.password
        print(namespace)

        conn_string = "%s://%s:%s@%s:%s/%s" % (
            "postgresql+psycopg2",
            namespace.user,
            namespace.password,
            namespace.host,
            namespace.port,
            namespace.database
        )

        engine = create_engine(conn_string)

        engine.connect()

        Session.configure(bind=engine)
        session = Session()

        db_script_path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "scripts",
                "pgsql",
                "public.sql"
            )
        )

        def fix_command(sql_command):
            return sql_command.replace("<NUTRAC_USER>", namespace.user)

        run_script(db_script_path, session, handle_command=fix_command)

        user = UserBase()
        user.uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, "http://localhost"))
        user.username = "nutracmin"
        user.password = bcrypt.encrypt("nutracpass")
        user.private_key = generate_private_key()

        session.add(user)
        session.commit()
        session.close()

        logger.info("Creating the NuTrac database.")
