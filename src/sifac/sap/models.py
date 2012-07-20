# -*- coding: utf-8 -*-

"""

sifac.sap.models
============

All the models to communicate with the sifac application are defined here:

    * CostCenter
    * Eotp
    * Fund
    * FunctionalDomain

"""

import logging
import re
from django.utils.translation import ugettext_lazy as _

from .db import SifacDB


LOGGER = logging.getLogger(__name__)


class SifacModel(object):
    """ Base model for Sifac models. All models define here must subclass
    this model

    .. py:attribute:: _db_connection

        the connection to the SIFAC sap client

    .. py:attribute:: _table

        the table to querying on (this must be defined in subclasses)

    .. py:attribute:: _columns

        a list of columns that contains the wanted data (this must be defined
        in subclasses)

    .. py:attribute:: verbose_name

        the translated model instance's name

    """

    _db_connection = SifacDB()
    _table = ""
    _columns = []
    verbose_name = ""

    def __init__(self, *args, **kwargs):
        super(SifacModel, self).__init__()

    @classmethod
    def _query_result(cls, filters):
        """
        Use the SIFAC connection to execute query and give the result back

            :param filters: SIFAC filters to filter data
            :type filters: tuple of strings
            :rtype: a list of strings

        """
        return cls._db_connection.query(cls._table, cls._columns, *filters)

    @classmethod
    def __get_structured_informations(cls, filters, pattern, data_structure):
        """
        Arrange data retrieved from a SIFAC database query and give the result
        back as the wanted data structure

            :param filters: SIFAC filters to filter data directly with the
                query
            :type filters: tuple of strings
            :param pattern: a pattern to filter values retrieved from query
            :type pattern: string
            :data_structure: the data structure type to return
            :type data_structure: iterable (list or dict for the moment)
            :raises: NotImplementedError when the type of data structure wanted
                isn't yet available
            :rtype: iterable

        """
        model_structure = data_structure()
        matcher = re.compile(pattern) if pattern else None
        separator_pattern = re.compile('(?<=\S)(\s{2,})(?=\S)')
        for value in cls._query_result(filters):
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
        Query on SIFAC model and return a dict of data

            :param filters: SIFAC filters to filter data directly with the
                query
            :type filters: tuple of strings
            :param pattern: a pattern to filter values retrieved from query
            :type pattern: string
            :raises: NotImplementedError when using this method with the
                SifacModel base class directly
            :returns: a dictionnary with model instance id as key and the
                instance as value
            :rtype: dict

        """
        if cls.__name__ == 'SifacModel':
            raise NotImplementedError(
                "This method should not be called with the SifacModel class")
        return cls.__get_structured_informations(filters, pattern, dict)

    @classmethod
    def get_list(cls, filters=(), pattern=""):
        """
        Query on SIFAC model and return a dict of data

            :param filters: SIFAC filters to filter data directly with the
                query
            :type filters: tuple of strings
            :param pattern: a pattern to filter values retrieved from query
            :type pattern: string
            :raises: NotImplementedError when using this method with the
                SifacModel base class directly
            :rtype: list of instances

        """
        if cls.__name__ == 'SifacModel':
            raise NotImplementedError(
                "This method should not be called with the SifacModel class")
        return cls.__get_structured_informations(filters, pattern, list)

    @classmethod
    def set_connection(cls, connection):
        """ 
        Used to set the sifac connection

            :param connection: the sifac connection instance
            :type connection: a saprfc connection instance
            
        """
        cls._db_connection = SifacDB(conn=connection)


class CostCenter(SifacModel):
    """
    Model to manage cost centers

        .. py:attribute:: code

            the cost center code 

        .. py:attribute:: _table

            the table for cost centers (CSKS)

        .. py:attribute:: _columns

            the columns for cost center (KOSTL)

    """

    _table = "CSKS"
    _columns = ["KOSTL"]
    verbose_name = _("Cost center")

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
    Model to manage Eotp

        .. py:attribute:: code

            the eotp code

        .. py:attribute:: cost_center

            the cost center instance the eotp is attached (could be None)

        .. py:attribute:: _table

            the table for eotp (PRPS)

        .. py:attribute:: _columns

            the columns for eotp (POSID, FKSTL)

    """

    _table = "PRPS"
    _columns = ["POSID", "FKSTL"]
    verbose_name = _("Eotp")

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
    Model to manage funds

        .. py:attribute:: code

            the fund code

        .. py:attribute:: description

            the fund description

        .. py:attribute:: _table

            the table for fund (FMFINT)

        .. py:attribute:: _columns

            the columns for fund (FINCODE, BEZEICH)

    """

    _table = "FMFINT"
    _columns = ["FINCODE", "BEZEICH"]
    verbose_name = _("Fund")

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
    Model to manage functional domains

        .. py:attribute:: code

            the functional domain code

        .. py:attribute:: description

            the functional domain description

        .. py:attribute:: _table

            the table for functional domains (TFKBT)

        .. py:attribute:: _columns

            the columns for functional domains (FKBER, FKBTX)

    """

    _table = "TFKBT"
    _columns = ["FKBER", "FKBTX"]
    verbose_name = _("Functional domain")

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
