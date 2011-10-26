# -*- coding: utf-8 -*-

"""
sifacuds.middleware
=====================

Middleware to get back informations from sifac
"""

import saprfc
from sifacuds.models import Eotp, Cc

from django.conf import settings


class SifacUDSMiddleware(object):
    """
    """

    def process_request(self, request):
        """Loads sifac informations in session
        """        
                                                       
        if request.session.get('sifac_cc') == None or request.session.get('sifac_eotp') == None:
            
            list_sifac_cc = []   
            list_sifac_eotp = []               
                                   
            conn = saprfc.conn(ashost=settings.ASHOST, sysnr=settings.SYSNR, client=settings.CLIENT,
                   user=settings.USER, passwd=settings.PASSWF, trace=1)
            
            try:
            
                conn.connect()    
        
                # CC
                iface = conn.discover("RFC_READ_TABLE")
                iface.query_table.setValue("FMHISV")
                iface.FIELDS.setValue(["FISTL","PARENT_ST"])
                iface.OPTIONS.setValue( ["PARENT_ST = 'PAIE'"] )
        
                conn.callrfc( iface )
                       
                for x in iface.DATA.value:
                    res = x.split()
                    cc = Cc(res[0],res[1])
                    list_sifac_cc.append(cc)       
        
                # EOTP
                iface2 = conn.discover("RFC_READ_TABLE")
                iface2.query_table.setValue("PRPS")
                iface2.FIELDS.setValue(["POSID","FKSTL"])
        
                conn.callrfc( iface2 )
                              
                for x2 in iface2.DATA.value:
                    res2 = x2.split()
                    if len(res2) == 2:
                        eotp = Eotp(res2[0],res2[1])
                        list_sifac_eotp.append(eotp)
                
                request.session['sifac_cc'] = list_sifac_cc        
                request.session['sifac_eotp'] = list_sifac_eotp    
                
            except Exception:
                pass
            
            finally:
                conn.close()
                
                
                
            
            