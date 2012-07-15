# -*- coding: utf-8 -*-

"""
"""

import logging
import re

from .db import SifacDB


logger = logging.getLogger(__name__)


class SifacModel(object):
    """
    """
    _db_connection = SifacDB()

    @classmethod
    def _query_result(cls, *filters):
        return cls._db_connection.query(cls._table, cls._columns, *filters)

    @classmethod
    def get_dict(cls, filters=(), pattern=""):
        raise NotImplementedError()

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        raise NotImplementedError()


class CostCenter(SifacModel):
    """
    """

    _table = "CSKS"
    _columns = ["KOSTL"]

    def __init__(self, code, *args, **kwargs):
        super(CostCenter, self).__init__(*args, **kwargs)
        self.code = code

    @classmethod
    def get_dict(cls, filters=(), pattern=""):
        """
        """
        cc_dict = {}
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            cost_center_code = value.split()[0]
            if not matcher or matcher.match(cost_center_code):
                cc_dict[cost_center_code] = cls(cost_center_code)
        return cc_dict

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        """
        """
        cc_list = []
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            cost_center_code = value.split()[0]
            if not matcher or matcher.match(cost_center_code):
                cc_list.append(cls(cost_center_code))
        return cc_list

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

    @classmethod
    def get_dict(cls, filters=(), pattern=""):
        """
        """
        eotp_dict = {}
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            try:
                codes = value.split()
                if len(codes) > 2:
                    raise Exception()
                if not matcher or matcher.match(codes[0]):
                    cost_center_code = codes[1] if len(codes) > 1 else None
                    eotp_dict[codes[0]] = cls(codes[0], cost_center_code)
            except:
                logger.warn(
                    "Problem to split returning eotp {0}".format(value)
                )
        return eotp_dict

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        """
        """
        eotp_list = []
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            try:
                codes = value.split()
                if len(codes) > 2:
                    raise Exception()
                if not matcher or matcher.match(codes[0]):
                    cost_center_code = codes[1] if len(codes) > 1 else None
                    eotp_list.append(cls(codes[0], cost_center_code))
            except:
                logger.warn(
                    "Problem to split returning eotp {0}".format(value)
                )
        return eotp_list

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

    @classmethod
    def get_dict(cls, filters=(), pattern=""):
        """
        """
        fund_dict = {}
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            splitted_result = value.split()
            fund_code = splitted_result[0]
            if not matcher or matcher.match(fund_code):
                fund_dict[fund_code] = cls(
                    fund_code, 
                    ' '.join(splitted_result[1:]).decode('iso-8859-15')
                )
        return fund_dict

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        """
        """
        fund_list = []
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            splitted_result = value.split()
            fund_code = splitted_result[0]
            if not matcher or matcher.match(fund_code):
                fund_list.append(cls(
                    fund_code, 
                    ' '.join(splitted_result[1:]).decode('iso-8859-15')
                ))
        return fund_list

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

    @classmethod
    def get_dict(cls, filters=(), pattern=""):
        """
        """
        funcdom_dict = {}
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            splitted_result = value.split()
            functional_domain_code = splitted_result[0]
            if not matcher or matcher.match(functional_domain_code):
                funcdom_dict[functional_domain_code] = cls(
                    functional_domain_code,
                    ' '.join(splitted_result[1:]).decode('iso-8859-15')
                )
        return funcdom_dict

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        """
        """
        funcdom_list = []
        matcher = re.compile(pattern) if pattern else None
        for value in cls._query_result(*filters):
            splitted_result = value.split()
            functional_domain_code = splitted_result[0]
            if not matcher or matcher.match(functional_domain_code):
                funcdom_list.append(cls(
                    functional_domain_code, 
                    ' '.join(splitted_result[1:]).decode('iso-8859-15')
                ))
        return funcdom_list

    def __repr__(self):
        return '<FunctionalDomain: {0.code}>'.format(self)

    def __str__(self):
        return '{0} - {1}'.format(self.code, self.description.encode('utf-8'))

    def __unicode__(self):
        return u'{0.code} - {0.description}'.format(self)
