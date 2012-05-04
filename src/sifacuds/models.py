# -*- coding: utf-8 -*-

"""
"""

class Cc(object):
    """
    """

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return 'Cc: {0}'.format(self.code)


class Eotp(object):
    """
    """

    def __init__(self, code, cc=None):
        self.code = code
        self.cc = cc

    def __repr__(self):
        return 'Eotp: {0.code} {1}'.format(self, '- {0.cc}'.format(self)  if self.cc else "")


class Fund(object):
    """
    """

    def __init__(self, code, desc):
        self.code = code
        self.desc = desc

    def __repr__(self):
        return 'Fund: {0.code} - {0.desc}'.format(self)


class FuncDom(object):
    """
    """

    def __init__(self ,code, desc):
        self.code = code
        self.desc = desc

    def __repr__(self):
        return 'FuncDom: {0.code} - {0.desc}'.format(self)
