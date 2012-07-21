# -*- coding: utf-8 -*-

from django.utils import unittest
from sifac.models import SAPModelFilter
from sifac.models import SAPQueryFilter


class SAPModelFilterTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        self.cost_center = SAPModelFilter.objects.create(
            sap_model_name="CostCenter", pattern="")
        self.eotp = SAPModelFilter.objects.create(sap_model_name="Eotp",
                pattern="")
        self.filters = [
            SAPQueryFilter.objects.create(sap_model=self.eotp,
                query_filter="APIE1%"),
            SAPQueryFilter.objects.create(sap_model=self.eotp,
                query_filter="APIE2%")]

    def tearDown(self):
        self.cost_center.delete()
        for filter_ in self.filters:
            filter_.delete()
        self.filters = None
        self.eotp.delete()


    def test_filters(self):
        """ Test accessing filters from an SAPModelFilter instance
        """
        self.assertListEqual(list(self.cost_center.get_query_filters()), [])
        self.assertListEqual(list(self.eotp.get_query_filters()), [
            filter_.query_filter for filter_ in self.filters])

    def test_filters_as_string(self):
        """ Test formatting filters as a string for admin interface
        """
        self.assertEqual(self.cost_center.get_query_filters_as_string(), u"")
        self.assertEqual(self.eotp.get_query_filters_as_string(), 
            u"APIE1%, APIE2%")

    def test_printing(self):
        """ Test human readable printing of instances
        """
        self.assertEqual(unicode(self.cost_center), u"CostCenter filter")
        self.assertEqual(unicode(self.filters[0]), u"APIE1% on Eotp")
        from django.utils.translation import ugettext
        self.assertEqual(
            ugettext(self.cost_center.human_sap_model_name()),
            u"Cost center")

    def test_sap_model_unicity(self):
        """ Test creating filters for an already saved sap model
        """
        from django.db import IntegrityError
        self.assertRaises(IntegrityError, SAPModelFilter.objects.create,
                sap_model_name="CostCenter", pattern="LA[0-9]{2}")
