# -*- coding: utf-8 -*-

"""
"""

from django import forms
from .models import SAPModelFilter
from .utils import get_sap_models


def get_unfiltered_sap_models():
    """
    Used to define choices for the form select box. Possible values are the
    subclasses of the base sap model class that are not already filtered
    """

    already_filtered = SAPModelFilter.objects.values_list('sap_model_name',
                                                          flat=True)

    is_filtered = lambda member_name: member_name in already_filtered

    return [(model.__name__, model.verbose_name) for model in get_sap_models()
            if not is_filtered(model.__name__)]


class SAPModelFilterForm(forms.ModelForm):
    """
    """

    def __init__(self, *args, **kwargs):
        super(SAPModelFilterForm, self).__init__(*args, **kwargs)
        self.fields['sap_model_name'].widget = forms.Select(
                choices=get_unfiltered_sap_models())

    class Meta:
        model = SAPModelFilter
