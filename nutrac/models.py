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
from datetime import datetime
from sqlalchemy.types import INT, Text, Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import DefaultClause
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from uuid import UUID as UUID_PY


class Base(DeclarativeBase):
    pass


class UserBase(Base):

    __tablename__ = "nuser"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID_PY] = mapped_column(UUID, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    email1: Mapped[str] = mapped_column(String(255), nullable=True)
    unconfirmed_email: Mapped[str] = mapped_column(String(255),
                                                   nullable=True)
    confirm_email_token: Mapped[str] = mapped_column(String(120),
                                                     nullable=True)
    reset_password_token: Mapped[str] = mapped_column(String(120),
                                                      nullable=True)
    login_count: Mapped[int] = mapped_column(INT, DefaultClause("0"),
                                             nullable=False)
    current_login_ip: Mapped[str] = mapped_column(String(50), nullable=True)
    last_login_ip: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(15), DefaultClause("'en'"),
                                          nullable=False)
    getting_started: Mapped[str] = mapped_column(Boolean,
                                                 DefaultClause("False"),
                                                 nullable=False)
    private_key: Mapped[str] = mapped_column(Text, nullable=False)
    enabled: Mapped[str] = mapped_column(Boolean, DefaultClause("True"),
                                         nullable=False)
    deleted: Mapped[str] = mapped_column(Boolean, DefaultClause("False"),
                                         nullable=False)
    created_at: Mapped[datetime] = mapped_column(
            TIMESTAMP, DefaultClause("CURRENT_TIMESTAMP"), nullable=False)
    modified_at: Mapped[datetime] = mapped_column(
            TIMESTAMP, DefaultClause("CURRENT_TIMESTAMP"), nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(
            TIMESTAMP, DefaultClause("CURRENT_TIMESTAMP"), nullable=True)
    reset_password_sent_at: Mapped[datetime] = mapped_column(
            TIMESTAMP, DefaultClause("CURRENT_TIMESTAMP"), nullable=True)
    last_seen_at: Mapped[datetime] = mapped_column(
            TIMESTAMP, DefaultClause("CURRENT_TIMESTAMP"), nullable=True)
