# -*- coding: utf-8 -*-

"""
"""

import unittest
import fudge
from sifac.models import SifacModel
from sifac.db import SifacDB


class TestSifacModel(unittest.TestCase):
    """ Testing the cost center model
    """

    def test_failures_getting_data(self):
        """ Test failures on retrieving data with base model class
        """
        message = "This method should not be called with the SifacModel class"
        self.assertRaisesRegexp(
            NotImplementedError, message, SifacModel.get_list)
        self.assertRaisesRegexp(
            NotImplementedError, message, SifacModel.get_dict)

    def test_set_connection(self):
        """ Test setting the sifac connection on base class
        """
        sifac_conn = fudge.Fake('saprfc.conn')
        SifacModel.set_connection(sifac_conn)
        self.assertIsInstance(SifacModel._db_connection, SifacDB)
