# -*- coding: utf-8 -*-

"""
"""

class Cc():
    
    def __init__(self,code,parent):
        self.code = code
        self.parent = parent
        
    def __repr__(self):
        return 'Cc: %s - %s ' % (self.code, self.parent) 
    
    

class Eotp():
    
    def __init__(self,code,cc):
        self.code = code
        self.cc = cc
        
    def __repr__(self):
        return 'Eotp: %s - %s' % (self.code, self.cc)
    