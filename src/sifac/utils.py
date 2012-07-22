# -*- coding: utf-8 -*-

"""
"""

import types
from .sap import models as sap_models


def get_sap_models():
    """
    Get implemented SAP models
    """

    get_member = lambda member_name: getattr(sap_models, member_name)

    is_a_class = lambda member_name: isinstance(get_member(member_name),
                                                types.TypeType)

    is_sifac_model = lambda member_name: is_a_class(member_name) and \
            issubclass(get_member(member_name), sap_models.SifacModel) and \
            member_name != 'SifacModel'

    return (get_member(model_name) for model_name in dir(sap_models)
            if is_sifac_model(model_name))
