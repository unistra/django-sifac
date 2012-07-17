# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

path = '{0}/src'.format(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

setup(
    name = 'Django-SIFAC',
    version = '0.2.0',
    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = [
        'saprfc'
    ],


    author = 'Morgan Bohn',
    author_email = 'morgan.bohn@unistra.fr',
    description = 'A SAP API for SIFAC',
    license = 'CeCILL-B',
    keywords = 'sifac sap django',
    url = 'https://github.com/unistra/django-sifac/'
)
