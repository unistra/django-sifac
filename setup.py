# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


setup(
    name='django-sifac',
    version='0.3.2',
    packages=find_packages(),

    install_requires=[
        'saprfc'
    ],

    package_data={
        'sifac': [
            'locale/*/LC_MESSAGES/*.po',
            'locale/*/LC_MESSAGES/*.mo',
        ]

    },

    author='Morgan Bohn',
    author_email='morgan.bohn@unistra.fr',
    maintainer='Arnaud Grausem',
    maintainer_email='arnaud.grausem@unistra.fr',
    description='A SAP API for SIFAC',
    license='CeCILL-B',
    keywords='sifac sap django',
    url='https://github.com/unistra/django-sifac/'
)
