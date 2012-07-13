# -*- coding: utf-8 -*-

"""
"""

import unittest
from itertools import izip

try:
    utils = __import__('utils')
except ImportError:
    pass
from sifacuds.models import CostCenter

values_from_sifac = [
    'ART',
    'ART2PI',
    'ART3DP1',
    'ART4DU2',
    'CHM1LI0121',
    'CHM2RS',
    'CHM3DP1',
    'CHM3DP2',
    'CHM3DP3',
    'CHM3DP4',
    'CHM3DPC',
    'CHM3MRC',
    'DALR4',
    'DPICDE0700',
    'DUNAUD',
    'DUNFCT',
    'EAV',
    'EAVCOM',
    'EAVDO',
    'EAVDOC',
    'EAVFOR',
    'EAVJPO',
    'EAVJU',
    'EAVLY',
    'EAVMR',
    'EAVNCT',
    'EAVPIL',
    'EAVQM',
    'EAVTF',
    'ECP1LI0440',
    'ECP1LI0443',
    'ECP2COM',
    'ECP2FORU',
    'ECP3CPI',
    'ECP3DP7',
    'EOT1LI0040',
    'EOT1LI0153',
    'EOT2PI',
    'EOT3DNC',
    'EOT3ING',
    'ESP1LI0331',
    'HIS3MR4',
    'HIS3MR5',
    'HIS3MR6',
    'IFM2DPA',
    'IFM2FCA',
    'IFM3DNC4',
    'IFM3DNC5',
    'IFM3DNC6',
    'IFM3MRBIL',
    'IFM51ED1',
    'IFM51ED2',
    'IFM52ND',
    'IHA1TE0320',
    'IHA2CO',
    'LVI2RES',
    'LVI3DP31',
    'LVI3DP35',
    'LVI3DP44',
    'LVI3DP5',
    'LVI5CFL',
    'LVI8BIB11',
    'LVI8BIB9',
    'MED1LI0550',
    'MED1LI0580',
    'MED1LI0591',
    'PAIE7R1051',
    'PAIE7R1052',
    'PAIE7R1061',
    'PAIE7R3041',
    'PAIE7R3042',
    'PAIE7R3211',
    'PAIE7R3212',
    'PAIE7RIGB1',
    'PAIE7RIGB2',
    'PAIE7RISI2',
    'PAIE7RMAI1',
    'PAIE7RMAI2',
    'PREEMP',
    'R101SEGE04',
    'R304MAIBIB',
    'R309EOTE03',
    'R309EOTE04',
    'R309EOTE05',
    'R309EOTE06',
    'R309EOTE07',
    'R309EOTE08',
    'R309EOTE09',
    'R309EOTE10',
    'R309EOTE11',
    'R316CHME02',
    'R316CHME05',
    'R317CHM',
    'R318ECP',
    'SCD2API',
    'SCD2BPI',
    'SCD2CPI',
    'SCD2DPI',
    'SCD8BIBA',
    'SCD8BIBB',
    'SCD8SAN1',
    'SCD8SAN2',
    'SEG3LCC',
    'SEG3MR1',
    'SEG3MR12',
    'SEG3MR31',
    'V417PHAN',
    'VCDPUEMRN'
]

test_data = (
    {'filters': (), 'pattern': '', 'from_sifac': values_from_sifac,
        'expected': values_from_sifac},
    {'filters': ('SCD%', 'SEG%'), 'pattern': '', 
        'from_sifac': values_from_sifac, 'expected': ['SCD2API', 'SCD2BPI', 
            'SCD2CPI', 'SCD2DPI', 'SCD8BIBA', 'SCD8BIBB', 'SCD8SAN1', 
            'SCD8SAN2', 'SEG3LCC', 'SEG3MR1', 'SEG3MR12', 'SEG3MR31']},
    {'filters': ('R%', ), 'pattern': 'R[0-9]{3}[A-Z]{4}[0-9]{2}', 
        'from_sifac': values_from_sifac, 'expected': [
            'R101SEGE04', 'R309EOTE03', 'R309EOTE04', 'R309EOTE05',
            'R309EOTE06', 'R309EOTE07', 'R309EOTE08', 'R309EOTE09', 
            'R309EOTE10', 'R309EOTE11', 'R316CHME02', 'R316CHME05']},
    {'filters': ('LALA%1'), 'pattern': '', 'from_sifac': values_from_sifac, 
        'expected': []},
    {'filters': (), 'pattern': '', 'from_sifac': [], 'expected': []}
)


class TestCostCenter(unittest.TestCase):
    """ Testing the cost center model
    """

    @utils.faking_query
    def test_get_list(self):
        """ Test retrieving a list of cost centers
        """
        for data in test_data:
            result = CostCenter.get_list(filters=data.items(), 
                pattern=data['pattern'])
            self.assertIsInstance(result, type([]))
            for cost_center, code in izip(result, data['expected']):
                self.assertIsInstance(cost_center, CostCenter)
                self.assertEqual(cost_center.code, code)

    @utils.faking_query
    def test_get_dict(self):
        """ Test retrieving a dict of cost centers
        """
        for data in test_data:
            result = CostCenter.get_dict(filters=data.items(),
                    pattern=data['pattern'])
            self.assertIsInstance(result, type({}))
            for key_code, code in zip(sorted(result), data['expected']):
                cost_center = result[key_code]
                self.assertIsInstance(cost_center, CostCenter)
                self.assertEqual(cost_center.code, code)
                self.assertEqual(key_code, code)

    def test_printing(self):
        """ Test built-in printing functions for cost center model
        """
        cost_center = CostCenter('HISTO3')
        self.assertEqual(str(cost_center), 'HISTO3')
        self.assertEqual(unicode(cost_center), 'HISTO3'.decode('utf-8'))
        self.assertEqual(repr(cost_center), '<CostCenter: HISTO3>')
