=====
Usage
=====

Django-SIFAC provides models for accessing data from financial repository
called SIFAC. This repository is deployed in many french universities. For the 
moment, it isn't possible to write but only to retrieve data as lists or
dictionnaries

Querying with models
====================

All of the models exposed on the models module works the same. You can retrieve
data as lists or dicts. For example, for cost centers ::
    
    from sifac.sap.models import CostCenter, Fund

    cost_centers = CostCenter.get_list()
    funds = Fund.get_dict()


Filters
-------

In some cases, we want to filter data directly with the database query.
Querying on Sifac (SAP) with the Python saprfc library is not very efficient.
To filter, we only use the "%" char ::

    from sifac.sap.models import Eotp

    eotp = Eotp.get_dict(filters=('V99%', 'R301%'))


Result will only contain Eotp whose code starts with 'V99' or 'R301'


Pattern
-------

In other cases, it might be difficult to apply filters, so we introduce
patterns to filter list of retrieving data from. Be careful and use this with 
precaution because all of the tuples of a table will be loaded before the 
pattern will be applied. It can be a good idea to use global filters first and
then to apply a pattern ::

    from sifac.sap.models import CostCenter

    cost_centers = CostCenter.get_dict(filters=('V99%'),
        pattern='V99[0-6]')


This will filter cost centers whose code starts with 'V99' and then apply the
pattern the will match only those that begins with V99 followed by a number
betwwen 0 and 6. With only filters, this can be done as ::

    filters = ('V990%', 'V991%', 'V992%', 'V993%', 'V994%', 'V995%', 'V996%')
    cost_centers = CostCenter.get_dict(filters=filters)


Querying directly
=================

You can access to low level functionnalities on the SifacDB class directly.
With an instance of the this class, querying on sifac database is possible if
you know on which table and columns the data you wanted are located. ::

    from sifac.sap.db import SifacDB

    sifac_connection = SifacDB()
    results = sifac_connection.query("CSKS", ["KOSTL"], filters=('V99%'))


For example, this will return a list of filtered cost centers. The result of
this function is a list of badly formatted strings due to the saprfc library. I
really recommend to use high level models.

Use with the Sifac service
==========================

If you've already added filters for a SAP model, you can access directly to the
filtered data with the sifac service instance. Here, we create some filters for
the example ::

    from sifac.models import SAPModelFilter, SAPQueryFilter

    model_filter = SAPModelFilter.objects.create(sap_model_name='CostCenter')
    query_filter = SAPQueryFilter.objects.create(sap_model=model_filter,
        query_filter='PAIE1%')

With the sifac Service, you can retrieve directly the filtered data ::

    from sifac.service import SifacService

    sifac_service = SifacService()
    filtered_cost_center = sifac_service.get_filtered_cost_center_list()

Directly with the SAP models, you should do ::

    from sifac.sap.models import CostCenter
    from sifac.models import SAPModelFilter

    sap_filters = SAPModelFilter.objects.get(sap_model_name='CostCenter')
    filtered_cost_centers = CostCenter.get_list(
        filters=sap_filters.get_query_filters(), pattern=sap_filters.pattern)

