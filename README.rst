============
Django-SIFAC
============

Django-SIFAC is a API to interact with the financial repository called SIFAC
and deployed in many french universities. It is not really a django specific
app for SIFAC but it's easy to use with Django. For the moment, only data on 
cost centers, eotp, funds and functional domains are available for reading, but 
not for writing.

Installation
------------

To install the saprfc library, please refer to this `documentation
<http://www.piersharding.com/download/python/doc/html/building-unix.html>`_.
If you place the rcfsdk headers in the right place, you can run this command ::

    pip install django-sifac


Integrate with your django app
------------------------------

You need to add this lines to the settings file of your django project ::

    ASHOST = '' #  Hostname to connect (i.e sap.host.com)
    SYSNR = '' # System number to connect to (i.e '00')
    CLIENT = '' # Client number logged in (i.e '500')
    USER = '' # Username
    PASSWF = '' # Password

If you want to use the SAP models filter application, you must activate the
administration interface in the settings file of your project and add the sifac
application in your INSTALLED_APPS setting ::

    INSTALLED_APPS = (
        ...,
        django.contrib.admin,
        ...,
        sifac
    )

To create tables needed by the sifac application, syncing your database is
necessary ::
    
    $> python manage.py syncdb


Basic usage
-----------

If you're using filters and pattern for your SAP Models (or not), it is really
easy to use the library to retrieve filtered data. Filters and patterns for
each SAP models can be created or updated in the admnistration interface ::

    from sifac import service

    sifac_service = SifacService()
    cost_centers = sifac_service.get_filtered_cost_center_list()
