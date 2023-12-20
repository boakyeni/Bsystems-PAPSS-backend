from django.db.models import Q
from django_countries.fields import CountryField
from rest_framework import filters
import fuzzywuzzy.fuzz as fuzz


class FuzzySearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        if not search_terms:
            return queryset

        q_objects = Q()
        for term in search_terms:
            for field in view.search_fields:
                # Check if the field is a CountryField
                model_field = queryset.model._meta.get_field(field)
                if isinstance(model_field, CountryField):
                    # Handle CountryField specifically
                    for obj in queryset:
                        country = getattr(obj, field)
                        if country and (
                            fuzz.partial_ratio(country.name.lower(), term.lower()) > 60
                            or fuzz.partial_ratio(country.code.lower(), term.lower())
                            > 60
                        ):
                            q_objects |= Q(pk=obj.pk)
                else:
                    # Handle other fields
                    q_objects |= Q(**{f"{field}__icontains": term})
                    for obj in queryset:
                        field_value = getattr(obj, field)
                        if (
                            isinstance(field_value, str)
                            and fuzz.partial_ratio(field_value.lower(), term.lower())
                            > 60
                        ):
                            q_objects |= Q(pk=obj.pk)

        return queryset.filter(q_objects).distinct()
