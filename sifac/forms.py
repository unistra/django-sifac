# -*- coding: utf-8 -*-

"""
sifac.forms
===========

Custom form for the administration GUI
"""

from django import forms
from .models import SAPModelFilter
from .utils import get_sap_models


def get_unfiltered_sap_models():
    """
    Used to define choices for the form select box. Possible values are the \
    subclasses of the base sap model class that are not already filtered.
    
        :returns: formatted list for form choices including the model's name
            and the translation of the model verbose name
        :rtype: a list of tuples

    """

    already_filtered = SAPModelFilter.objects.values_list('sap_model_name',
                                                          flat=True)

    is_filtered = lambda member_name: member_name in already_filtered

    return [(model.__name__, model.verbose_name) for model in get_sap_models()
            if not is_filtered(model.__name__)]


class SAPModelFilterForm(forms.ModelForm):
    """
    Form displayed in the admin GUI interfaxce. It adds a select widget on
    SAP Model field to display only available SAP models that are not already
    filtered.
    """

    def __init__(self, *args, **kwargs):
        super(SAPModelFilterForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields['sap_model_name'].widget.attrs['readonly'] = True
        else:
            self.fields['sap_model_name'].widget = forms.Select(
                choices=get_unfiltered_sap_models())

    class Meta:
        model = SAPModelFilter
