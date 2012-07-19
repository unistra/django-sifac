# -*- coding: utf-8 -*-

"""
sifac.admin
===========

Administration GUI configuration for filters and pattern
"""


from django.contrib import admin
from .models import SAPModelFilter
from .models import SAPQueryFilter


class SAPQueryFilterInline(admin.TabularInline):
    """
    """
    model = SAPQueryFilter


class SAPModelFilterAdmin(admin.ModelAdmin):
    """
    """
    inlines = [SAPQueryFilterInline]


admin.site.register(SAPModelFilter, SAPModelFilterAdmin)
