# -*- coding: utf-8 -*-

"""
"""
import unittest

try:
    utils = __import__('utils')
except ImportError:
    pass
from sifacuds.models import CostCenter


test_data = (
    {'filters': (), 'pattern': '', 'from_sifac': ['HISTO6', 'HISTO7'],
        'expected': ['HISTO6', 'HISTO7']},
    {'filters': ('LALA%1',), 'pattern': '', 
        'from_sifac': ['LALA1', 'HISTO6', 'HISTO7'], 'expected': ['LALA1']},
    {'filters': ('HISTO%', ), 'pattern': 'H[A-Z]{3}.[1-5]',
        'from_sifac': ['LALA1', 'HISTO1', 'HISTO2', 'HISTO6', 'HISTN3'],
        'expected': ['HISTO1', 'HISTO2']},
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
            for cost_center, code in zip(result, data['expected']):
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
        """
        """
        cost_center = CostCenter('HISTO3')
        self.assertEqual(str(cost_center), 'HISTO3')
        self.assertEqual(unicode(cost_center), 'HISTO3'.decode('utf-8'))
        self.assertEqual(repr(cost_center), '<CostCenter: HISTO3>')
