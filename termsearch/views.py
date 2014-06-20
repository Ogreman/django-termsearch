# -*- coding: utf-8 -*-
import operator

from django.db.models import Q


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