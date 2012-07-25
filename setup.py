# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
    name = 'django-sifac',
    version = '0.2.1',
    packages = ['sifac', 'sifac.sap'],
    package_dir = {'': 'src'},

    install_requires = [
        'saprfc'
    ],

    package_data = {
        'sifac': [
            'locale/*/LC_MESSAGES/*.po',
            'locale/*/LC_MESSAGES/*.mo',
        ]

    },

    author = 'Morgan Bohn',
    author_email = 'morgan.bohn@unistra.fr',
    description = 'A SAP API for SIFAC',
    license = 'CeCILL-B',
    keywords = 'sifac sap django',
    url = 'https://github.com/unistra/django-sifac/'
)
