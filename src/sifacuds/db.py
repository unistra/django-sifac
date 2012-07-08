# -*- coding: utf-8 -*-

import logging
import re
import saprfc

from django.conf import settings


logger = logging.getLogger(__name__)


class SifacDB(object):
    """ Services to get information from SIFAC """

    def __init__(self, conn=None):
        """ Init conn attr """
        self.__conn = conn

    def __connect(self):
        """ Connection to SIFAC """
        if self.__conn is None:
            try:
                self.__conn = saprfc.conn(ashost=settings.ASHOST, sysnr=settings.SYSNR, client=settings.CLIENT,
                    user=settings.USER, passwd=settings.PASSWF, trace=0)
                self.__conn.connect()
            except Exception as e:
                logger.critical("Can't connect to Sifac DB: %s" % str(e))

    def __close(self):
        """ Close connection from SIFAC """
        try:
            self.__conn.close()
            self.__conn = None
        except Exception as e:
            logger.error("Can't close Sifac connection: %s" % str(e))

    def query(self, table, columns, *filters):
        """
        """
        try:
            self.__connect()

            iface = self.__conn.discover("RFC_READ_TABLE")
            iface.query_table.setValue(table)
            iface.FIELDS.setValue(columns)
            if filters:
                query = []
                for index, filter_ in enumerate(filters):
                    query.append("{0} LIKE '{1}'".format(columns[0], filter_))
                    if index < len(filters) - 1:
                        query.append("OR")
                iface.OPTIONS.setValue(query)

            self.__conn.callrfc( iface )
            values = iface.DATA.value

        except Exception as e:
            logger.error("Can't exexcute query on Sifac DB: %s" % str(e))

        finally:
            self.__close()

        return values
