# -*- coding: utf-8 -*-

"""
sifac.admin
===========

Administration GUI configuration for filters and pattern
"""


from django.contrib import admin
from .models import SAPModelFilter
from .models import SAPQueryFilter
from .forms import SAPModelFilterForm


class SAPQueryFilterInline(admin.TabularInline):
    """
    """
    model = SAPQueryFilter


class SAPModelFilterAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('human_sap_model_name', 'get_query_filters_as_string',
                    'pattern')
    form = SAPModelFilterForm
    inlines = [SAPQueryFilterInline]


admin.site.register(SAPModelFilter, SAPModelFilterAdmin)
