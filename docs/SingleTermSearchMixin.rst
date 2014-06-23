=============================
SingleTermSearchMixin
=============================

Filter on a single model field.


Use the ``string`` representation of the field and the lookup type to filter the queryset::

    from termsearch.views import SingleTermSearchMixin

    class MyListView(SingleTermSearchMixin, ListView):

        model = MyModel
        term = "title"
        lookup = "iexact"

Raises an ImproperlyConfigured exception when missing the required attribute ``term``.

``lookup`` is optional and defaults to "exact" when not provided.