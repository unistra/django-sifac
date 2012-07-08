# -*- coding: utf-8 -*-

import logging
import re
import saprfc
from django.conf import settings



logger = logging.getLogger(__name__)


class SifacUDSService(object):
    """ Services to get information from SIFAC """

    def __init__(self, conn = None):
        """ Init conn attr """
        self.__conn = conn

    def __connect(self):
        """ Connection to SIFAC """
        if self.__conn is None:
            try:
                self.__conn = saprfc.conn(ashost=settings.ASHOST, sysnr=settings.SYSNR, client=settings.CLIENT,
                    user=settings.USER, passwd=settings.PASSWF, trace=0)
                self.__conn.connect()
            except Exception:
                pass

    def __close(self):
        """ Close connection from SIFAC """
        try:
            self.__conn.close()
            self.__conn = None
        except Exception:
            pass


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
            pass

        finally:
            self.__close()

        return values

    """
    def getDictFuncDom(self):
        dict_sifac_df = {}
        try:
            if self.__conn is None: self.__connectSifac()
            # FUND
            iface4 = self.__conn.discover("RFC_READ_TABLE")
            iface4.query_table.setValue("TFKBT")
            iface4.FIELDS.setValue(["FKBER","FKBTX"])
            self.__conn.callrfc( iface4 )
            for x in iface4.DATA.value:
                x_split = x.split()
                code = x_split[0]
                p= re.compile('^[0-9]{3}[A-Z]{2}')
                m = p.match(code)
                if m:
                    df = FuncDom(code, ' '.join(x_split).decode("iso-8859-15"))
                    dict_sifac_df[code] = df
        except Exception:
            pass
        finally:
            self.__closeSifac()
        return dict_sifac_df
    """
