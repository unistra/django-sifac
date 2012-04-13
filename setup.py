# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

path = '{0}/src'.format(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

setup(
    name = 'django-sifacuds',
    version = '0.0.8',
    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = [
        'saprfc'
    ],

    dependency_links =  [
        'http://pedago-pg728.u-strasbg.fr/python/snapshots'
    ],

    author = 'Morgan Bohn',
    author_email = 'morgan.bohn@unistra.fr',
    description = 'A SAP API for SIFAC UDS',
    license = 'Other',
    keywords = 'sifac sap django uds',
    url = ''

)
