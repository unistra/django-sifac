# -*- coding: utf-8 -*-

"""
"""

import re
import functools
import types
from .sap import models as sap_models
from .sap.db import SifacDB


def get_sap_models():
    """
    Get implemented SAP models
    """

    get_member = lambda member_name: getattr(sap_models, member_name)

    is_a_class = lambda member_name: isinstance(get_member(member_name),
                                                types.TypeType)

    is_sifac_model = lambda member_name: is_a_class(member_name) and \
            issubclass(get_member(member_name), sap_models.SifacModel) and \
            member_name != 'SifacModel'

    return (get_member(model_name) for model_name in dir(sap_models)
            if is_sifac_model(model_name))


def fake_db_query(cls, table, columns, *data):
    """ Fakes query on sifac database
    """
    data = dict(data)
    filters = [
        re.compile(filter_.replace('%', '.')) for filter_ in
        data.get('filters', [])
    ]
    filtered_values = []
    for value in data.get('from_sifac', []):
        for filter_ in filters:
            if filter_.match(value):
                filtered_values.append(value)
    if filters:
        data['from_sifac'] = filtered_values
    return data['from_sifac']


def faking_query(func):
    """ Replaces function that handles queries on sifac instance on the fly
    before launching any function that needs to execute queries
    """
    @functools.wraps(func)
    def wrapped(self):
        setattr(SifacDB, 'query', fake_db_query)
        return func(self)
    return wrapped
