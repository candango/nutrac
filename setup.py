#!/usr/bin/env python
#
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

import nutrac
from setuptools import setup, find_packages
import sys

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    print("error: Upgrade to a pip version newer than 10. Run \"pip install "
          "--upgrade pip\".")
    sys.exit(1)


# Solution from http://bit.ly/29Yl8VN
def resolve_requires(requirements_file):
    try:
        requirements = parse_requirements("./%s" % requirements_file,
                                          session=False)
        return [str(ir.req) for ir in requirements]
    except AttributeError:
        # for pip >= 20.1.x
        # Need to run again as the first run was ruined by the exception
        requirements = parse_requirements("./%s" % requirements_file,
                                          session=False)
        # pr stands for parsed_requirement
        return [str(pr.requirement) for pr in requirements]


with open("README.md", "r") as fh:
    long_description = fh.read()

# We still running: python setup.py sdist upload --repository=testpypi
# Twine isn't handling long_descriptions as per:
# https://github.com/pypa/twine/issues/262
setup(
    name="Nutrac",
    version="0.1",
    description="Nutrac is a trac multi-project and login manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=nutrac.__licence__,
    author=nutrac.get_author(),
    author_email=nutrac.get_author_email(),
    maintainer=nutrac.get_author(),
    maintainer_email=nutrac.get_author_email(),
    install_requires=resolve_requires("requirements.txt"),
    python_requires=">= 3.8",
    url="https://github.com/candango/nutrac",
    packages=find_packages(),
    package_dir={'nutrac': "nutrac"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Trac",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
