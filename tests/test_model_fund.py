# -*- coding: utf-8 -*-

"""
"""

import unittest
from itertools import izip
from sifac.models import Fund

utils = __import__('utils')


def expect_from(values):
    """
    """
    return [
        (value.split()[0], ' '.join(value.split()[1:]).decode('iso-8859-15'))
        for value in values
    ]

values_from_sifac = [
    '111       DGF',
    '112       Contrat',
    '12        Minist\xe8re sant\xe9',
    '13        Autres minist\xe8res',
    '14        Cr\xe9dits s\xe9curit\xe9',
    '15        Actions sp\xe9cifiques',
    '21        CNRS et instituts',
    '22        INSERM',
    '23        Autres org rech',
    '24        INRA',
    '311       MENESR (FNS)',
    '312       Org. de rech. (FNS)',
    "313       Fin. FNS via l'ANR",
    '321       MENESR (FRT)',
    '322       Org. de rech. (FRT)',
    "323       Fin. FRT via l'ANR",
    '41        Minist\xe8res',
    '42        Via ANR',
    '43        Org. de rech.',
    '44        Collectivit\xe9s terr.',
    '51        R\xe9gions',
    '52        Autres coll. Terr.',
    '611       MENESR',
    '612       Min. industrie',
    '613       Min. D\xe9fense',
    '614       Autres minist\xe8res',
    '621       CNRS',
    '622       INSERM',
    '623       Autres org. rech.',
    '624       INRA',
    '625       ANR',
    '631       R\xe9gions',
    '632       Autres',
    '64        Entreprises',
    "641       Taxe d'apprentissage",
    '642       ASSEDIC',
    '643       OPCA',
    "651       PCRDT de l'UE",
    '652       Fonds str. eur.',
    '653       Autres ressources'
]

test_data = (
    {'filters': (), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': expect_from(values_from_sifac)},
    {'filters': ('64%', '65%'), 'pattern': '',
        'from_sifac': values_from_sifac, 'expected': expect_from([
            '64        Entreprises', "641       Taxe d'apprentissage",
            '642       ASSEDIC', '643       OPCA', "651       PCRDT de l'UE",
            '652       Fonds str. eur.', '653       Autres ressources'])},
    {'filters': ('6%', ), 'pattern': '.*1$', 'from_sifac': values_from_sifac,
        'expected': expect_from([
            '611       MENESR', '621       CNRS',
            '631       R\xe9gions', "641       Taxe d'apprentissage",
            "651       PCRDT de l'UE"])},
    {'filters': (), 'pattern': '^[0-9]{2}$', 'from_sifac': values_from_sifac,
        'expected': expect_from([
            '12        Minist\xe8re sant\xe9',
            '13        Autres minist\xe8res',
            '14        Cr\xe9dits s\xe9curit\xe9',
            '15        Actions sp\xe9cifiques', '21        CNRS et instituts',
            '22        INSERM', '23        Autres org rech', '24        INRA',
            '41        Minist\xe8res', '42        Via ANR',
            '43        Org. de rech.', '44        Collectivit\xe9s terr.',
            '51        R\xe9gions', '52        Autres coll. Terr.',
            '64        Entreprises'])},
    {'filters': ('LALA%1',), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': []},
    {'filters': (), 'pattern': '[A-Z]{3}', 'from_sifac': values_from_sifac,
        'expected': []},
    {'filters': (), 'pattern': '', 'from_sifac': [], 'expected': []}
)


class TestFund(unittest.TestCase):
    """ Testing the fund model
    """

    @utils.faking_query
    def test_get_list(self):
        """ Test retrieving a list of funds
        """
        for data in test_data:
            result = Fund.get_list(
                filters=data.items(), pattern=data['pattern'])
            self.assertIsInstance(result, type([]))
            for fund, values in izip(result, data['expected']):
                self.assertIsInstance(fund, Fund)
                self.assertEqual(fund.code, values[0])
                self.assertEqual(fund.description, values[1])

    @utils.faking_query
    def test_get_dict(self):
        """ Test retrieving a dict of funds
        """
        for data in test_data:
            result = Fund.get_dict(
                filters=data.items(), pattern=data['pattern'])
            self.assertIsInstance(result, type({}))
            for key_code, values in zip(sorted(result), data['expected']):
                fund = result[key_code]
                self.assertIsInstance(fund, Fund)
                self.assertEqual(fund.code, values[0])
                self.assertEqual(fund.description, values[1])
                self.assertEqual(key_code, values[0])

    def test_printing(self):
        """ Test built-in printing functions for fund model
        """
        fund = Fund("641", "Taxe d'apprentissage")
        self.assertEqual(str(fund), "641 - Taxe d'apprentissage")
        self.assertEqual(unicode(fund), "641 - Taxe d'apprentissage"
            .decode('utf-8'))
        self.assertEqual(repr(fund), '<Fund: 641>')
