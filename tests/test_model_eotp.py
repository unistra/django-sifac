# -*- coding: utf-8 -*-

"""
"""

import unittest
from itertools import izip
import re
from sifac.models import Eotp

utils = __import__('utils')


def expect_from(values):
    """
    """
    split_pattern = re.compile("(?<=\S)\s{2,}(?=\S)")
    return [split_pattern.split(value) for value in values]


values_from_sifac = [
    'A08RAN55                R101SEG',
    'A08RAN56                R314ESB',
    'A08RAN58                R314ESB',
    'A08RAN60                R416PHA',
    'A08RAN61                R324PHI',
    'A08RAN6404',
    'A08RAN77/01',
    'A08RAN77/02',
    'A08RAN78                R324PHI',
    'A08RAN82                R305VIE',
    'A09R8A12/01',
    'A09R8A13/01',
    'A09R8A21/01',
    'A09R8A22/01',
    'A09R8A27/01',
    'A11R304D                R304MAI',
    'A11R417B                R417PHA',
    'A12N325A                V325PHIN',
    'A12N415A                V415PHAN',
    'A12R304A                R304MAI',
    'A12R316A                R316CHM',
    'A12R316B                R316CHM',
    'A12R316E                R316CHM',
    'A12R320B                R320ECP',
    'A12R320C                R320ECP',
    'A12R415A                R415PHA',
    'A12R416A                R416PHA',
    'A12R417A                R417PHA',
    'C12RDGPP                R219THP',
    'C12RUETP                R219THP',
    'M11MD131CLAVP           MED5FCFI',
    'M11MD132BOURC           MED5FCFI',
    'M11MD133GICQU           MED5FCFI',
    'M11MD134ARMSP           MED5FCFI',
    'M11MED92 ROUL           MED5FCFI',
    'M11PSY01LES1',
    'M11PSY02OPDU',
    'M11PSY03STX1',
    'M11PSY04OEFC',
    'M12PSY01MMSN',
    'V99LRMNG407             V308PSYL1',
    'V99N0003                V415PHAN',
    'V99N0009                V308PSYN',
    'V99N0015                V205SOCN',
    'V99N0016',
    'V99N0022                V415PHAN',
    'V99N0031                V316CHMN',
    'V99N0037                V101SEGN',
    'V99N0039                V409MEDN',
    'V99N0056                V308PSYN',
    'V99N0063                V415PHAN',
    'V99N0066                V312ESPN',
    'V99N0072                V305VIEN',
    'V99N0086                V312ESPN',
    'V99N0087                V415PHAN',
    'V99N0092                V310EOTN',
    'V99N0094                V321ISIN',
    'V99N0096                V312ESPN',
    'V99N0098                V416PHAN'
]

test_data = (
    {'filters': (), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': expect_from(values_from_sifac)},
    {'filters': ('M11M%',), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': expect_from([
            'M11MD131CLAVP           MED5FCFI',
            'M11MD132BOURC           MED5FCFI',
            'M11MD133GICQU           MED5FCFI',
            'M11MD134ARMSP           MED5FCFI',
            'M11MED92 ROUL           MED5FCFI'])},
    {'filters': ('V99%', ), 'pattern': '.*6$',
        'from_sifac': values_from_sifac,
        'expected': expect_from([
            'V99N0016',
            'V99N0056                V308PSYN',
            'V99N0066                V312ESPN',
            'V99N0086                V312ESPN',
            'V99N0096                V312ESPN'])},
    {'filters': ('R%'), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': expect_from([])},
    {'filters': (), 'pattern': '', 'from_sifac': [],
        'expected': expect_from([])}
)


class TestEotp(unittest.TestCase):
    """ Testing the eotp model
    """

    @utils.faking_query
    def test_get_list(self):
        """ Test retrieving a list of eotps
        """
        for data in test_data:
            result = Eotp.get_list(
                filters=data.items(), pattern=data['pattern'])
            self.assertIsInstance(result, type([]))
            for eotp, codes in zip(result, data['expected']):
                self.assertIsInstance(eotp, Eotp)
                self.assertEqual(eotp.code, codes[0])
                if len(codes) == 2:
                    self.assertEqual(eotp.cost_center.code, codes[1])
                else:
                    self.assertIsNone(eotp.cost_center)

    @utils.faking_query
    def test_get_dict(self):
        """ Test retrieving a dict of eotps
        """
        for data in test_data:
            result = Eotp.get_dict(
                filters=data.items(), pattern=data['pattern'])
            self.assertIsInstance(result, type({}))
            for key_code, codes in izip(sorted(result), data['expected']):
                eotp = result[key_code]
                self.assertIsInstance(eotp, Eotp)
                self.assertEqual(eotp.code, codes[0])
                if len(codes) == 2:
                    self.assertEqual(eotp.cost_center.code, codes[1])
                else:
                    self.assertIsNone(eotp.cost_center)
                self.assertEqual(key_code, codes[0])

    def test_printing(self):
        """ Test built-in printing functions for eotp model
        """
        eotp = Eotp('V99N0096', 'V312ESPN')
        self.assertEqual(str(eotp), 'V99N0096 (V312ESPN)')
        self.assertEqual(unicode(eotp), 'V99N0096 (V312ESPN)'.decode('utf-8'))
        self.assertEqual(repr(eotp), '<Eotp: V99N0096>')
