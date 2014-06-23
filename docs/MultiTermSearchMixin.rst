=============================
MultiTermSearchMixin
=============================

Filter on multiple model fields.


Use a ``list`` of model fields to use in the search::

    from termsearch.views import MultiTermSearchMixin

    class MyListView(MultiTermSearchMixin, ListView):

        model = MyModel
        terms = ["title", "author", "content"]
        lookup = "iexact"

Each term will filter the queryset using the ``lookup`` attribute.

Raises an ImproperlyConfigured exception when missing the required attribute ``terms``.

As with SingleTermSearchMixin, ``lookup`` is optional and defaults to "exact" when not provided.

