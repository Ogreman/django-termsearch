# -*- coding: utf-8 -*-
import operator

from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured


class _BaseSearchMixin(object):

    lookup = "exact"

    def get_queryset(self):
        self.qs = super(_BaseSearchMixin, self).get_queryset()
        q = self.request.GET.get("q")
        if q:
            self._apply_filters(q)
        return self.qs

    def _apply_filters(self, q):
        raise ImproperlyConfigured("Base class implementation not supported")


class SingleTermSearchMixin(_BaseSearchMixin):

    def _apply_filters(self, q):
        try:
            self.qs = self.qs.filter(
                **{
                    "{0}__{1}".format(self.term, self.lookup): q,
                }
            )
        except AttributeError:
            raise ImproperlyConfigured("Expected `term` attribute")


class MultiTermSearchMixin(_BaseSearchMixin):

    def _apply_filters(self, q):
        try:
            queries = reduce(operator.or_,
                (
                    Q(**{
                        "{0}__{1}".format(
                            term, self.lookup
                        ): q,
                    })
                    for term in self.terms
                )
            )
            self.qs = self.qs.filter(queries)
        except AttributeError:
            raise ImproperlyConfigured("Expected `terms` attribute")


class MapTermSearchMixin(_BaseSearchMixin):

    def _apply_filters(self, q):
        try:
            queries = Q()
            for term, lookup in self.term_mapping.items():
                queries.add(
                    Q((
                        '{0}__{1}'.format(term, lookup),
                        q
                    )),
                    queries.OR
                )
            self.qs = self.qs.filter(queries)
        except AttributeError:
            raise ImproperlyConfigured("Expected `term_mapping` attribute")


class TermSearchMixin(object):
    """
    Mixin for providing a GET search functionality to views.

    Must implement one of the following:

        term + lookup (str),
        terms (list)
        term_mapping (dict)

    Examples given below:

        terms = [
            "title",
            "tags__name"
        ]
        term_mapping = {
            "title": "icontains",
            "tags__name": "iexact",
        }
    """

    lookup = "exact"

    def get_queryset(self):
        queryset = super(TermSearchMixin, self).get_queryset()
        q = self.request.GET.get("q")
        if q:

            if hasattr(self, "terms"):
                queries = reduce(operator.or_,
                    (
                        Q(**{
                            "{0}__{1}".format(
                                term, self.lookup
                            ): q,
                        })
                        for term in self.terms
                    )
                )
                return queryset.filter(queries)

            if hasattr(self, "term_mapping"):
                queries = Q()
                for term, lookup in self.term_mapping.items():
                    queries.add(
                        Q((
                            '{0}__{1}'.format(term, lookup),
                            q
                        )),
                        queries.OR
                    )
                return queryset.filter(queries)

            if hasattr(self, "term"):
                return queryset.filter(
                    **{
                        "{0}__{1}".format(self.term, self.lookup): q,
                    }
                )

        return queryset