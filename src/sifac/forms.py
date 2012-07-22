# -*- coding: utf-8 -*-

"""
"""

import types
from django import forms
from .models import SAPModelFilter
from .sap import models as sap_models


def get_unfiltered_sap_models():
    """
    Used to define choices for the form select box. Possible values are the
    subclasses of the base sap model class that are not already filtered
    """

    already_filtered = SAPModelFilter.objects.values_list('sap_model_name',
                                                          flat=True)

    get_member = lambda member_name: getattr(sap_models, member_name)

    is_a_class = lambda member_name: isinstance(get_member(member_name),
                                                (types.TypeType,
                                                 types.ClassType))

    is_sifac_model = lambda member_name: is_a_class(member_name) and \
            issubclass(get_member(member_name), sap_models.SifacModel) and \
            member_name != 'SifacModel'

    is_filtered = lambda member_name: member_name in already_filtered

    return [(model_name, get_member(model_name).verbose_name) 
            for model_name in dir(sap_models)
            if is_sifac_model(model_name) and not is_filtered(model_name)]


class SAPModelFilterForm(forms.ModelForm):
    """
    """

    def __init__(self, *args, **kwargs):
        super(SAPModelFilterForm, self).__init__(*args, **kwargs)
        self.fields['sap_model_name'].widget = forms.Select(
                choices=get_unfiltered_sap_models())

    class Meta:
        model = SAPModelFilter
