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

from firenado.util.sqlalchemy_util import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BIGINT, Date, INT, Text, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index, DefaultClause
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID


class UserBase(Base):

    __tablename__ = "nuser"

    id = Column("id", BIGINT, primary_key=True)
    uuid = Column("uuid", UUID, nullable=False)
    username = Column("username", String(100), nullable=False)
    password = Column("password", String(255), nullable=False)
    email = Column("email", String(255), nullable=True)
    email1 = Column("email1", String(255), nullable=True)
    unconfirmed_email = Column("unconfirmed_email", String(255), nullable=True)
    confirm_email_token = Column("confirm_email_token", String(120),
                                 nullable=True)
    reset_password_token = Column("reset_password_token", String(120),
                                  nullable=True)
    login_count = Column("login_count", INT, DefaultClause("0"),
                         nullable=False)
    current_login_ip = Column("current_login_ip", String(50), nullable=True)
    last_login_ip = Column("last_login_ip", String(50), nullable=True)
    language = Column("language", String(15), DefaultClause("en"),
                      nullable=False)
    getting_started = Column("getting_started", Boolean,
                             DefaultClause('False'), nullable=False)
    private_key = Column("private_key", Text, nullable=False)
    enabled = Column("enabled", Boolean, DefaultClause('True'), nullable=False)
    deleted = Column("deleted", Boolean, DefaultClause('False'),
                     nullable=False)
    created_at = Column('created_at', TIMESTAMP(),
                        DefaultClause('CURRENT_TIMESTAMP'), nullable=False)
    modified_at = Column('modified_at', TIMESTAMP(),
                         DefaultClause('CURRENT_TIMESTAMP'), nullable=False)
    deleted_at = Column('deleted_at', TIMESTAMP(), nullable=True)
    reset_password_sent_at = Column('reset_password_sent_at', TIMESTAMP(),
                                    nullable=True)
    last_seen_at = Column('last_seen_at', TIMESTAMP(), nullable=True)
