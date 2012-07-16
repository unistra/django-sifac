# -*- coding: utf-8 -*-

"""
"""

import logging
import re

from .db import SifacDB


LOGGER = logging.getLogger(__name__)


class SifacModel(object):
    """
    """

    _db_connection = SifacDB()
    _table = ""
    _columns = []

    @classmethod
    def _query_result(cls, *filters):
        return cls._db_connection.query(cls._table, cls._columns, *filters)

    @classmethod
    def __get_structured_informations(cls, filters, pattern, data_structure):
        model_structure = data_structure()
        matcher = re.compile(pattern) if pattern else None
        separator_pattern = re.compile('(?<=\S)(\s{2,})(?=\S)')
        for value in cls._query_result(*filters):
            model_infos = [
                column.decode('iso-8859-15') for column
                in separator_pattern.split(value)
                if len(column) != column.count(' ')
            ]
            model_id = model_infos[0]
            if not matcher or matcher.match(model_id):
                instance = cls(*model_infos)
                if isinstance(model_structure, type({})):
                    model_structure[model_id] = instance
                elif isinstance(model_structure, type([])):
                    model_structure.append(instance)
                else:
                    raise NotImplementedError(
                        "The {0} data structure is not managed yet"
                        .format(data_structure)
                    )
        return model_structure

    @classmethod
    def get_dict(cls, filters=(), pattern=""):
        """
        """
        if cls.__name__ == 'SifacModel':
            raise NotImplementedError(
                "This method should not be called with the SifacModel class")
        return cls.__get_structured_informations(filters, pattern, dict)

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        """
        """
        if cls.__name__ == 'SifacModel':
            raise NotImplementedError(
                "This method should not be called with the SifacModel class")
        return cls.__get_structured_informations(filters, pattern, list)


class CostCenter(SifacModel):
    """
    """

    _table = "CSKS"
    _columns = ["KOSTL"]

    def __init__(self, code, *args, **kwargs):
        super(CostCenter, self).__init__(*args, **kwargs)
        self.code = code

    def __repr__(self):
        return '<CostCenter: {0}>'.format(self.code)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return unicode(self.code)


class Eotp(SifacModel):
    """
    """

    _table = "PRPS"
    _columns = ["POSID", "FKSTL"]

    def __init__(self, code, cost_center=None, *args, **kwargs):
        super(Eotp, self).__init__(*args, **kwargs)
        self.code = code
        self.cost_center = CostCenter(cost_center) if cost_center else None

    def __repr__(self):
        return '<Eotp: {0.code}>'.format(self)

    def __str__(self):
        return '{0.code}{1}'.format(
            self, '' if not self.cost_center else ' ({0.code})'
            .format(self.cost_center)
        )

    def __unicode__(self):
        return u'{0.code}{1}'.format(
            self, '' if not self.cost_center else u' ({0.code})'
            .format(self.cost_center)
        )


class Fund(SifacModel):
    """
    """

    _table = "FMFINT"
    _columns = ["FINCODE", "BEZEICH"]

    def __init__(self, code, description, *args, **kwargs):
        super(Fund, self).__init__(*args, **kwargs)
        self.code = code
        self.description = description

    def __repr__(self):
        return '<Fund: {0.code}>'.format(self)

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.description.encode('utf-8'))

    def __unicode__(self):
        return u'{0.code} - {0.description}'.format(self)


class FunctionalDomain(SifacModel):
    """
    """

    _table = "TFKBT"
    _columns = ["FKBER", "FKBTX"]

    def __init__(self, code, description, *args, **kwargs):
        super(FunctionalDomain, self).__init__(*args, **kwargs)
        self.code = code
        self.description = description

    def __repr__(self):
        return '<FunctionalDomain: {0.code}>'.format(self)

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.description.encode('utf-8'))

    def __unicode__(self):
        return u'{0.code} - {0.description}'.format(self)
