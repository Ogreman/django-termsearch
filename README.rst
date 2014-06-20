=============================
dj-termsearch
=============================

Simple term searches for Django CBV's.

Documentation
-------------

The full documentation is at https://dj-termsearch.readthedocs.org.

Quickstart
----------

Install dj-termsearch::

    pip install dj-termsearch

Add ``"termsearch"`` to your ``INSTALLED_APPS`` then just add ``TermSearchMixin`` to a view and go::

    from django.db import models

    from termsearch.views import TermSearchMixin

    class MyModelListView(TermSearchMixin, ListView):
        model = MyModel
        term = "title"
        lookup = "iexact"
    
Features
--------

* TODO
