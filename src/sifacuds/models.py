# -*- coding: utf-8 -*-

"""
"""

class Cc():
    
    def __init__(self,code):
        self.code = code
                
    def __repr__(self):
        return 'Cc: %s' % (self.code) 
    
    

class Eotp():
    
    def __init__(self,code,cc):
        self.code = code
        self.cc = cc
        
    def __repr__(self):
        return 'Eotp: %s - %s' % (self.code, self.cc)
    
    

class Fund():
    
    def __init__(self,code,desc):
        self.code = code
        self.desc = desc
        
    def __repr__(self):
        return 'Fund: %s - %s' % (self.code, self.desc)    
    
    
class FuncDom():
    
    def __init__(self,code,desc):
        self.code = code
        self.desc = desc
        
    def __repr__(self):
        return 'FuncDom: %s - %s' % (self.code, self.desc)    
    