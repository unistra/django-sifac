# -*- coding: utf-8 -*-

"""
sifacuds.middleware
=====================

Middleware to get back informations from sifac
"""

import saprfc
from sifacuds.models import Eotp, Cc, Fund, FuncDom

from django.conf import settings


class SifacUDSMiddleware(object):
    """
    """

    def process_request(self, request):
        """Loads sifac informations in session
        """        
                                                       
        if request.session.get('sifac_cc') == None or request.session.get('sifac_eotp') == None or request.session.get('sifac_fund') == None or request.session.get('sifac_df') == None:
            
            list_sifac_cc = []   
            list_sifac_eotp = []              
            dict_sifac_fund = {}   
            dict_sifac_df = {}
                                   
            conn = saprfc.conn(ashost=settings.ASHOST, sysnr=settings.SYSNR, client=settings.CLIENT,
                   user=settings.USER, passwd=settings.PASSWF, trace=0)
            
            try:
            
                conn.connect()    
        
                ##################################################### CC
                iface = conn.discover("RFC_READ_TABLE")
                iface.query_table.setValue("CSKS")
                iface.FIELDS.setValue(["KOSTL"])
                iface.OPTIONS.setValue( ["PRCTR LIKE 'PAIE%'"] )
        
                conn.callrfc( iface )
                       
                for x in iface.DATA.value:
                    res = x.split()
                    cc = Cc(res[0])
                    list_sifac_cc.append(cc)       
        
                ##################################################### EOTP
                iface2 = conn.discover("RFC_READ_TABLE")
                iface2.query_table.setValue("PRPS")
                iface2.FIELDS.setValue(["POSID","FKSTL"])
        
                conn.callrfc( iface2 )
                              
                for x2 in iface2.DATA.value:
                    res2 = x2.split()
                    if len(res2) == 2:
                        eotp = Eotp(res2[0],res2[1])
                        list_sifac_eotp.append(eotp)
                        
                        
                ##################################################### FUND                
                iface3 = conn.discover("RFC_READ_TABLE")
                iface3.query_table.setValue("FMFINT")
                iface3.FIELDS.setValue(["FINCODE","BEZEICH"])
                
                conn.callrfc( iface3 )
                
                for x in iface3.DATA.value:
                    x_split = x.split()
                    code = x_split[0]
                    fund = Fund(code, ' '.join(x_split).decode("iso-8859-15"))
                    dict_sifac_fund[code] = fund
                    
                ##################################################### DF
                iface4 = conn.discover("RFC_READ_TABLE")
                iface4.query_table.setValue("TFKBT")
                iface4.FIELDS.setValue(["FKBER","FKBTX"])
                
                conn.callrfc( iface4 )
                
                for x in iface4.DATA.value:
                    x_split = x.split()
                    code = x_split[0]
                    df = FuncDom(code, ' '.join(x_split).decode("iso-8859-15"))
                    dict_sifac_df[code] = df                
                        
                
                request.session['sifac_cc'] = list_sifac_cc        
                request.session['sifac_eotp'] = list_sifac_eotp   
                request.session['sifac_fund'] = dict_sifac_fund
                request.session['sifac_df'] = dict_sifac_df
                
            except Exception:
                pass
            
            finally:
                conn.close()
                
                
                
            
            