# -*- coding: utf-8 -*-

"""
sifac.models
============

This module defines the models that store filters and pattern used to querying
on sifac database.
"""


from django.db import models
from django.utils.translation import ugettext_lazy as _

from .sap import models as sap_models


class SAPModelFilter(models.Model):
    """
    Define pattern to apply to a SAP query result

        .. py:attribute:: sap_model_name
            
            The SAP model's name to consider

        .. py:attribute:: pattern

            The pattern to apply to result of a SAP query

    """

    sap_model_name = models.CharField(max_length=30,
                                      verbose_name=_('SAP Model name'),
                                      unique=True)
    pattern = models.CharField(max_length=255, blank=True,
                               verbose_name=_('Pattern'))

    class Meta:
        verbose_name = _('SAP Model filter')
        verbose_name_plural = _('SAP Model filters')
        ordering = ['sap_model_name']

    def __unicode__(self):
        return u'{0} filter'.format(self.sap_model_name)

    def get_query_filters(self):
        """
        Returns query filters saved for this SAP model

            :rtype: a list of string

        """
        return self.filters.values_list('query_filter', flat=True)

    def get_query_filters_as_string(self):
        """
        Returns a formatted string of query filters saved for this SAP model.
        Used in the admin GUI interface.

            :returns: a list of query filters as a coma separated string
            :rtype: string

        """
        return  ', '.join(self.get_query_filters())
    get_query_filters_as_string.short_description = _('Filters')

    def human_sap_model_name(self):
        """
        Returns human localized readable words to describe SAP models. Used in
        the administration GUI interface.

            :rtype: string

        """
        return getattr(sap_models, self.sap_model_name).verbose_name
    human_sap_model_name.short_description = _('SAP Model')


class SAPQueryFilter(models.Model):
    """
    Define filters to apply to a SAP query
        
        .. py:attribute:: sap_model

            The SAPModelFilter instance

        .. py:attribute:: query_filter

            The filter to apply to a SAP query

    """

    sap_model = models.ForeignKey(SAPModelFilter, related_name='filters',
                                  verbose_name=_('SAP Pattern filter'))
    query_filter = models.CharField(max_length=255, 
                                    verbose_name=_('SAP Query filter'))

    class Meta:
        verbose_name = _('SAP Query filter')
        verbose_name_plural = _('SAP Query filters')
        order_with_respect_to = 'sap_model'

    def __unicode__(self):
        return u'{0.query_filter} on {1.sap_model_name}'.format(
            self, self.sap_model)
