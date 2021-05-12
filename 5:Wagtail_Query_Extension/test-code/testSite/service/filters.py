from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.filters import BaseFilterBackend
from taggit.managers import TaggableManager
from wagtail.api.v2.filters import (FieldsFilter)

class ServiceFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        This performs field level filtering on the result set
        Eg: ?supportTag=moodAndMotivation,anxiety
        """
        fields = set(view.get_available_fields(queryset.model, db_fields_only=True))

        # Locale is a database field, but we provide a separate filter for it
        if 'locale' in fields:
            fields.remove('locale')

        for field_name, value in request.GET.items():
            if "__" in field_name:
                field_name_split = field_name.split("__") #split values around underscore.
                field_name = field_name_split[0] # set fieldname as should be in database.
                
            if field_name in fields:
                try:
                    field = queryset.model._meta.get_field(field_name)
                except LookupError:
                    field = None

                # Convert value into python
                try:
                    if isinstance(field, (models.BooleanField, models.NullBooleanField)):
                        value = parse_boolean(value)
                    elif isinstance(field, (models.IntegerField, models.AutoField)):
                        value = int(value)
                except ValueError as e:
                    raise BadRequestError("field filter error. '%s' is not a valid value for %s (%s)" % (
                        value,
                        field_name,
                        str(e)
                    ))

                if isinstance(field, TaggableManager):
                    # Here we will split our options and use them within a "In" search to act as an OR case.
                    tags = value.split(',')
                    queryset = queryset.filter(**{field_name+'__name__in': tags}).distinct()
                elif field_name_split is not None:
                    # We only enter here if we have received a value such as maxAge__gt, so we will query using that value, and the operator provided in the querystring.
                    queryset = queryset.filter(**{field_name+'__'+field_name_split[1]: value})
                else:
                    queryset = queryset.filter(**{field_name: value})

        return queryset