=============================
MapTermSearchMixin
=============================

Filter on multiple model fields with a ``lookup`` mapped to each.


Use a ``dict`` of model fields and lookups to use in the search::

    from termsearch.views import MapTermSearchMixin

    class MyListView(MapTermSearchMixin, ListView):

        model = MyModel
        term_mapping = {
            "title": "icontains",
            "tags__name": "iexact",
            "author__surname": "exact",
        }

Raises an ImproperlyConfigured exception when missing the required attribute ``term_mapping``.

