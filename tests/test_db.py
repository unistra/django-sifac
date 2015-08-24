# -*- coding: utf-8 -*-

import unittest

from sifac.sap.db import SifacDB


class TestSifacDB(unittest.TestCase):
    """ Test de la connection à Sifac
    """

    def setUp(self):
        self.sifac_db = SifacDB()

    def tearDown(self):
        del self.sifac_db

    def test_build_query_filters(self):
        """ Test de la construction de filtres de requête
        """
        test_data = [
            {'column': 'Test1', 'filters': ('TEST1%1', 'TEST2%1', 'TEST3%1'),
                'expected': [
                    "Test1 LIKE 'TEST1%1'", 'OR', "Test1 LIKE 'TEST2%1'", 'OR',
                    "Test1 LIKE 'TEST3%1'"]},
            {'column': 'Test2', 'filters': (), 'expected': []},
            {'column': 'Test3', 'filters': ('TEST4%1', ), 'expected': [
                "Test3 LIKE 'TEST4%1'"]}
        ]
        for data in test_data:
            self.assertEqual(self.sifac_db._build_filtered_query(
                data['column'], data['filters']), data['expected'])
