# -*- coding: utf-8 -*-

"""
sifac.sap.db
============

Module to manage connection and query on Sifac database
"""


import logging
import saprfc

try:
    from django.conf import settings
except ImportError:
    pass


LOGGER = logging.getLogger(__name__)


class SifacDB(object):
    """ Services to get information from SIFAC """

    def __init__(self, conn=None):
        """ Init conn attr """
        self.__conn = conn

    def connect(self):
        """ Connection to SIFAC """
        if self.__conn is None:
            try:
                self.__conn = saprfc.conn(
                    ashost=settings.ASHOST, sysnr=settings.SYSNR,
                    client=settings.CLIENT, user=settings.USER,
                    passwd=settings.PASSWF, trace=0
                )
            except Exception as sifac_exception:
                LOGGER.critical(
                    "Can't connect to Sifac DB: {0!s}".format(sifac_exception))
        self.__conn.connect()

    def close(self):
        """ Close connection from SIFAC """
        try:
            self.__conn.close()
        except Exception as sifac_exception:
            LOGGER.error(
                "Can't close Sifac connection: {0!s}".format(sifac_exception))

    @staticmethod
    def _build_filtered_query(column, filters):
        """
        Build formatted filters for the query
            
            :param colum: the column to apply filters
            :param filters: the filters to apply
            :type filters: list or tuple
            :rtype: list of formatted filters

        """
        query = []
        if filters:
            query = []
            for index, filter_ in enumerate(filters):
                query.append("{0} LIKE '{1}'".format(column, filter_))
                if index < len(filters) - 1:
                    query.append("OR")
        return query

    def query(self, table, columns, *filters):
        """ 
        Execute query on Sifac Database

            :param table: the table to query on
            :param columns: the columns value to get
            :type colums: list or tuple
            :param filters: the filters to apply to the query
            :type filters: list or tuple
            :returns: a list of formatted strings to split
            :rtype: list of strings

        """
        values = []

        try:
            self.connect()

            iface = self.__conn.discover("RFC_READ_TABLE")
            iface.query_table.setValue(table)
            iface.FIELDS.setValue(columns)

            query = self._build_filtered_query(columns[0], filters)
            if query:
                iface.OPTIONS.setValue(query)

            self.__conn.callrfc(iface)
            values = iface.DATA.value

        except Exception as sifac_exception:
            LOGGER.error(
                "Can't execute query on Sifac DB: {0!s}"
                .format(sifac_exception))

        finally:
            self.close()

        return values
