# -*- coding: utf-8 -*-

""" Utility functions for testing the sifacuds library
"""

import re
import functools
from sifacuds.db import SifacDB


def fake_db_query(cls, table, columns, *data):
    """ Fakes query on sifac database
    """
    data = dict(data)
    filters = [
        re.compile(filter_.replace('%', '.')) for filter_ in data['filters']
    ]
    filtered_values = []
    for value in data['from_sifac']:
        for filter_ in filters:
            if filter_.match(value):
                filtered_values.append(value)
    if filters:
        data['from_sifac'] = filtered_values
    return dict(data)['from_sifac']


def faking_query(func):
    """ Replaces function that handles queries on sifac instance on the fly
    before launching any function that needs to execute queries
    """
    @functools.wraps(func)
    def wrapped(self):
        setattr(SifacDB, 'query', fake_db_query)
        return func(self)
    return wrapped
