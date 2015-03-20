# -*- coding: utf-8 -*-

import fudge
from django.utils import unittest
from .forms import SAPModelFilterForm
from .models import SAPModelFilter
from .models import SAPQueryFilter
from .service import SifacService
from .service import SAPGetMethodService
from .utils import get_sap_models


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


class SAPModelFilterFormTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        self.dir_result = ['CostCenter', 'Eotp']


    @fudge.patch('__builtin__.dir')
    def test_get_sap_models(self, fake_dir):
        """
        """
        from django.utils.translation import ugettext as _
        expected = [('CostCenter', _('Cost center')), ('Eotp', _('Eotp'))]

        # faking dir builtin with a returned value
        (fake_dir.expects_call().with_arg_count(1)\
                .returns(self.dir_result))

        sap_models_form = SAPModelFilterForm()
        model_name_widget = sap_models_form['sap_model_name'].field.widget
        self.assertListEqual([
            (model_name, _(model_trans)) for model_name, model_trans in 
            model_name_widget.choices], expected)

    @fudge.patch('__builtin__.dir')
    def test_get_filtered_sap_models(self, fake_dir):
        """
        """
        from django.utils.translation import ugettext as _
        expected = [('CostCenter', _('Cost center'))]

        # add a new SAP model filter object that should not appear in results
        eotp_filter = SAPModelFilter.objects.create(sap_model_name='Eotp',
                                                    pattern="")

        (fake_dir.expects_call().with_arg_count(1)\
                .returns(self.dir_result))

        sap_models_form = SAPModelFilterForm()
        model_name_widget = sap_models_form['sap_model_name'].field.widget
        self.assertListEqual([
            (model_name, _(model_trans)) for model_name, model_trans in
            model_name_widget.choices], expected)

        eotp_filter.delete()


class TestSifacService(unittest.TestCase):
    """
    """

    def setUp(self):
        self.dir_result = ['CostCenter', 'Eotp']

    @fudge.patch('__builtin__.dir')
    def test_service(self, fake_dir):
        """
        """
        (fake_dir.expects_call().with_arg_count(1)\
                .returns(self.dir_result))
        service = SifacService()
        for function in ('get_filtered_cost_center_dict',
                         'get_filtered_cost_center_list',
                         'get_filtered_eotp_dict',
                         'get_filtered_eotp_list'):
            self.assertIsInstance(getattr(service, function),
                                  SAPGetMethodService)

    @fudge.patch('__builtin__.dir')
    def test_method(self, fake_dir):
        (fake_dir.expects_call().with_arg_count(1)\
                .returns(self.dir_result))
        cost_center_model = get_sap_models().next()

        method = SAPGetMethodService(cost_center_model, list)
        result = method()
        self.assertIsInstance(result, list)

        method = SAPGetMethodService(cost_center_model, dict)
        result = method()
        self.assertIsInstance(result, dict)
