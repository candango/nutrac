#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Nutrac Plugins',
    version='0.1',
    packages=['macros'],
    package_data={ 'macros': [ 'htdocs/*' ] },
    author='Piraz',
    author_email='piraz@candango.org',
    description='Nutrac plugins',
    license='Apache2.0',
    keywords='trac plugin theme acid',
    url='',
    classifiers=[
        'Framework :: Trac',
    ],
    install_requires=['Trac'],
    entry_points={
        'trac.plugins': [
            'Nutrac Milestone Query = macros.milestonequery',
        ]
    },
)
