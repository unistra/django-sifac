# -*- coding: utf-8 -*-

"""
sifac.models
============

This module defines the models that store filters and pattern used to querying
on sifac database.
"""


from django.db import models
from django.utils.translation import ugettext_lazy as _tr


class SAPModelFilter(models.Model):
    """
    Define pattern to apply to a SAP query result

        .. py:attribute:: sap_model
            
            The SAP model to consider

        .. py:attribute:: pattern

            The pattern to apply to result of a SAP query

    """

    sap_model_name = models.CharField(max_length=30,
                                      verbose_name=_tr('SAP Model name'),
                                      unique=True)
    pattern = models.CharField(max_length=255, blank=True,
                               verbose_name=_tr('Pattern'))

    class Meta:
        verbose_name = _tr('SAP Model filter')
        ordering = ['sap_model_name']

    def __unicode__(self):
        return u'{0} filter'.format(self.sap_model_name)

    def get_query_filter(self):
        """
        """
        return self.filters.values_list('query_filter', flat=True)


class SAPQueryFilter(models.Model):
    """
    Define filters to apply to a SAP query
        
        .. py:attribute:: sap_model

            The SAPModelFilter instance

        .. py:attribute:: query_filter

            The filter to apply to a SAP query

    """

    sap_model = models.ForeignKey(SAPModelFilter, related_name='filters',
                                  verbose_name=_tr('SAP Pattern filter'))
    query_filter = models.CharField(max_length=255, 
                                    verbose_name=_tr('SAP Query filter'))

    class Meta:
        verbose_name = _tr('SAP Query filter')
        order_with_respect_to = 'sap_model'

    def __unicode__(self):
        return u'{0.query_filter} on {1.sap_model_name}'.format(
            self, self.sap_model)
