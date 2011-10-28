# -*- coding: utf-8 -*-

import saprfc
import re
from sifacuds.models import Eotp, Cc, Fund, FuncDom

from django.conf import settings


class SifacUDSService(object):
    
    """ Services to get information from SIFAC """
    
    def __init__(self, conn = None):
        """ Init conn attr """
        self.__conn = conn
        
        
        
    def __connectSifac(self):
        """ Connection to SIFAC """
        try:
            self.__conn = saprfc.conn(ashost=settings.ASHOST, sysnr=settings.SYSNR, client=settings.CLIENT, user=settings.USER, passwd=settings.PASSWF, trace=0)
            self.__conn.connect()
        except Exception:
            pass
        
        
    def __closeSifac(self):
        """ Close connection from SIFAC """
        try:
            self.__conn.close()
            self.__conn = None
        except Exception:
            pass
    
    

    def getListCostCenterPaie(self):
        
        """ Get list CC PAIE{1,2,5,6,7}
        """
        
        list_sifac_cc = []                                    
            
        try:
            
            if self.__conn is None: self.__connectSifac()
                                
            # CC
            iface = self.__conn.discover("RFC_READ_TABLE")
            iface.query_table.setValue("CSKS")
            iface.FIELDS.setValue(["KOSTL"])
            iface.OPTIONS.setValue( ["KOSTL LIKE 'PAIE1%'", "OR", "KOSTL LIKE 'PAIE2%'", "OR", "KOSTL LIKE 'PAIE5%'", "OR", "KOSTL LIKE 'PAIE6%'", "OR", "KOSTL LIKE 'PAIE7%'"] )
        
            self.__conn.callrfc( iface )
                       
            for x in iface.DATA.value:
                res = x.split()
                cc = Cc(res[0])
                list_sifac_cc.append(cc)        
                          
        except Exception:
            pass
            
        finally:
            self.__closeSifac()
                 
        return list_sifac_cc    
    
    
    
    
    
    def getListEotp(self):
        
        """ Get Eotp with a CC
        """
        
        list_sifac_eotp = []                                 
            
        try:
            
            if self.__conn is None: self.__connectSifac()    
                    
            # EOTP
            iface2 = self.__conn.discover("RFC_READ_TABLE")
            iface2.query_table.setValue("PRPS")
            iface2.FIELDS.setValue(["POSID","FKSTL"])
        
            self.__conn.callrfc( iface2 )
                              
            for x2 in iface2.DATA.value:
                res2 = x2.split()
                if len(res2) == 2:
                    eotp = Eotp(res2[0],res2[1])
                    list_sifac_eotp.append(eotp)
                                       
        except Exception:
            pass
            
        finally:
            self.__closeSifac()
                
        return list_sifac_eotp
    




    def getDictFund(self):
        
        """ Get all fund
        """
        
        dict_sifac_fund = {}                                    
            
        try:
            
            if self.__conn is None: self.__connectSifac()   
                    
            # FUND
            iface3 = self.__conn.discover("RFC_READ_TABLE")
            iface3.query_table.setValue("FMFINT")
            iface3.FIELDS.setValue(["FINCODE","BEZEICH"])
                
            self.__conn.callrfc( iface3 )
                
            for x in iface3.DATA.value:
                x_split = x.split()
                code = x_split[0]
                fund = Fund(code, ' '.join(x_split).decode("iso-8859-15"))
                dict_sifac_fund[code] = fund
                                       
        except Exception:
            pass
            
        finally:
            self.__closeSifac()
                
        return dict_sifac_fund
    
    


    def getDictFuncDom(self):
        
        """ DF (code = 3 numbers + 2 chars alpha min)
        """
        
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
    
    
    