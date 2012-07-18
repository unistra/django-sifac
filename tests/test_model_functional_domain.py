# -*- coding: utf-8 -*-

"""
"""

import unittest
from itertools import izip
from sifac.sap.models import FunctionalDomain

utils = __import__('utils')


def expect_from(values):
    """
    """
    return [
        (value.split()[0], ' '.join(value.split()[1:]).decode('iso-8859-15'))
        for value in values
    ]

values_from_sifac = [
    '115INSST        INFO SERVEURS ET STOCKAGE',
    '115MOB          RH MOBILITE DES PERS',
    '115NETT         NETTOYAGE DES LOCAUX',
    '115PIL          PILOTAGE ANIM RES ACC PJT',
    '115POLS         POLITIQUE SOCIALE',
    '115REPR         REPROG IMPRI CONC GRAPH',
    '115RH           GESTION RH',
    '115RIADM        ADM SERVICES RI',
    '115RICOM        COMM EVT RI',
    '115RIPROJ       CONV ET PROJET RI',
    '115SERV         SERVICE INTERIEUR',
    '115SMUT         SERVICES COM MAG ATEL',
    '115TEL          TELEPHONIE',
    '201             Aides directes',
    '201ADM          ADM SERVICES VIE ETUD',
    '201AUT          AUTRES AIDES DIRECT',
    '201CULT         AIDES DIRECTES CULTU',
    '202             Aides indirectes',
    '202ADM          ADM SERVICES VIE ETUD',
    '202AUT          AUTRES AIDES IND',
    '202CULT         AIDES IND CULTU',
    '203             Sant\xe9 des \xe9tudiants',
    '203ADM          ADM SERVICES SANTE SPORT',
    '203HAND         FAV INSERT ETUD HAND',
    '203MED          MED PREVENTIVE ETUD',
    '203SPORT        SPORT',
    '204             Pil & anim des prog',
    'DZ1             0p\xe9 non d\xe9c 150(D\xe9p)',
    'DZ2             0p\xe9 non d\xe9c 231(D\xe9p)',
    'DZOP            DEP POUR ORDRE',
    'DZPI            DEP PREST INTERNES',
    'DZREGU          REGU INTERNES EN DEPENSES',
    'NA              Non Applicable',
    'RENC            REC ENCAISSABLES',
    'RZ1             0p\xe9 non d\xe9c 150(Rec)',
    'RZ2             0p\xe9 non d\xe9c 231(Rec)',
    'RZOP            REC POUR ORDRE',
    'RZPI            REC PRESTATIONS INTERNES',
    'RZREGU          REGU INTERNES EN RECETTES'
]

test_data = (
    {'filters': (), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': expect_from(values_from_sifac)},
    {'filters': ('115%', '203'), 'pattern': '',
        'from_sifac': values_from_sifac, 'expected': expect_from([
            '115INSST        INFO SERVEURS ET STOCKAGE',
            '115MOB          RH MOBILITE DES PERS',
            '115NETT         NETTOYAGE DES LOCAUX',
            '115PIL          PILOTAGE ANIM RES ACC PJT',
            '115POLS         POLITIQUE SOCIALE',
            '115REPR         REPROG IMPRI CONC GRAPH',
            '115RH           GESTION RH',
            '115RIADM        ADM SERVICES RI',
            '115RICOM        COMM EVT RI',
            '115RIPROJ       CONV ET PROJET RI',
            '115SERV         SERVICE INTERIEUR',
            '115SMUT         SERVICES COM MAG ATEL',
            '115TEL          TELEPHONIE',
            '203             Sant\xe9 des \xe9tudiants'])},
    {'filters': ('2%', ), 'pattern': '[A-Z]{4}',
        'from_sifac': values_from_sifac, 'expected': expect_from([
            '201CULT         AIDES DIRECTES CULTU',
            '202CULT         AIDES IND CULTU',
            '203HAND         FAV INSERT ETUD HAND'])},
    {'filters': (), 'pattern': '^[A-Z]{3}', 'from_sifac': values_from_sifac,
        'expected': expect_from([
            'DZOP            DEP POUR ORDRE',
            'DZPI            DEP PREST INTERNES',
            'DZREGU          REGU INTERNES EN DEPENSES',
            'RENC            REC ENCAISSABLES',
            'RZOP            REC POUR ORDRE',
            'RZPI            REC PRESTATIONS INTERNES',
            'RZREGU          REGU INTERNES EN RECETTES'])},
    {'filters': ('LALA%1',), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': []},
    {'filters': (), 'pattern': '[A-Z]{3}[0-9]{3}',
        'from_sifac': values_from_sifac, 'expected': []},
    {'filters': (), 'pattern': '', 'from_sifac': [], 'expected': []}
)


class TestFunctionalDomain(unittest.TestCase):
    """ Testing the functional domain model
    """

    @utils.faking_query
    def test_get_list(self):
        """ Test retrieving a list of functional domains
        """
        for data in test_data:
            result = FunctionalDomain.get_list(
                filters=data.items(), pattern=data['pattern'])
            self.assertIsInstance(result, type([]))
            for functional_domain, values in izip(result, data['expected']):
                self.assertIsInstance(functional_domain, FunctionalDomain)
                self.assertEqual(functional_domain.code, values[0])
                self.assertEqual(functional_domain.description, values[1])

    @utils.faking_query
    def test_get_dict(self):
        """ Test retrieving a dict of functional domains
        """
        for data in test_data:
            result = FunctionalDomain.get_dict(
                filters=data.items(), pattern=data['pattern'])
            self.assertIsInstance(result, type({}))
            for key_code, values in zip(sorted(result), data['expected']):
                functional_domain = result[key_code]
                self.assertIsInstance(functional_domain, FunctionalDomain)
                self.assertEqual(functional_domain.code, values[0])
                self.assertEqual(functional_domain.description, values[1])
                self.assertEqual(key_code, values[0])

    def test_printing(self):
        """ Test built-in printing functions for functional domain model
        """
        functional_domain = FunctionalDomain('RENC', 'REC ENCAISSABLES')
        self.assertEqual(str(functional_domain), "RENC - REC ENCAISSABLES")
        self.assertEqual(unicode(functional_domain), "RENC - REC ENCAISSABLES"
            .decode('utf-8'))
        self.assertEqual(repr(functional_domain), '<FunctionalDomain: RENC>')
