# -*- coding: utf-8 -*-

"""
sifac.service
=============

"""

import re
import types
from .models import SAPModelFilter
from .utils import get_sap_models


class SifacService(object):
    """
    """

    AVAILABLE_ITERABLE = [list, dict]

    def __new__(cls, *args, **kwargs):
        pattern = re.compile('([a-z])([A-Z])')
        for model in get_sap_models():
            for iterable_type in cls.AVAILABLE_ITERABLE:
                method = SAPGetMethodService(model, iterable_type)
                model_name = pattern.sub('\g<1>_\g<2>', model.__name__).lower()
                method_name = 'get_filtered_{0}_{1}'.format(model_name,
                        iterable_type.__name__)
                setattr(cls, method_name, method)
        return super(SifacService, cls).__new__(cls, *args, **kwargs)


class SAPGetMethodService(object):
    """
    """

    def __init__(self, sap_model, iterable_type):
        """
        .. py: attribute:: model_name
            
            The SAP model name

        .. py: attribute:: iterable_type
            
            The iterable type to return

        """
        self.sap_model = sap_model
        if isinstance(iterable_type, types.TypeType):
            self.iterable = iterable_type.__name__
        else:
            self.iterable = type(iterable_type).__name__

    def __call__(self):
        """
        Calls the appropriate function on the SAP model to retrieve formatted
        data
        """
        sap_model_func = getattr(self.sap_model,
                                 'get_{0}'.format(self.iterable))
        try:
            sap_model_filter = SAPModelFilter.objects.get(
                    sap_model_name=self.sap_model.__name__)
        except SAPModelFilter.DoesNotExist:
            return sap_model_func()
        else:
            return sap_model_func(filters=sap_model_filter.get_query_filters(),
                                  pattern=sap_model_filter.pattern) 
