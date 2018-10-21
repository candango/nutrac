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

from . import tasks
from firenado.management import ManagementCommand
from tornado import template
import os

NUTRAC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

loader = template.Loader(os.path.join(NUTRAC_ROOT, "templates", "management"))

nutracSubcommands = [
    ManagementCommand("createdb", "Create NuTrac database", "",
                      tasks=tasks.NutacCreateDatabaseTask),
]

ManagementCommand("nutrac", "Application related commands", loader.load(
    "nutrac_command_help.txt").generate(
    subcommands=nutracSubcommands), category="Nutrac",
                  sub_commands=nutracSubcommands)
