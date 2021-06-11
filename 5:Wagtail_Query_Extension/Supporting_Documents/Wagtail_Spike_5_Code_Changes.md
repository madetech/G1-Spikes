# Wagtail Code Changes

This document addressed the changes made to the Wagtail files. The pre-requisits for this can be found in the supporting_documents for the [first spike](../../1:Content_Query_and_Filtering/Content_Query_and_Filtering_Report.md) and the [second spike](../../2:Wagtail_Infrastructure_Requirements/Wagtail_Infrastructure_Requirements_Report.md).

## Service Model Changes

The first notable change made to the code will be found within our services model (`service/models.py`). 
Here we make 2 major changes:
* introduction of `minAge` and `maxAge`, 
* introduction of `serviceTags` and `supportTypeTags` using ClusterTaggableManager.

### Adding minAge and maxAge

These are simple fields that can be added, the changes to `service/models.py` are as so:

```Python
## testSite/service/models.py

class Service(Page):
    #existing variables, e.g. serviceId = models.CharField(max_length=100, unique=True)

    maxAge = models.IntegerField()
    minAge = models.IntegerField()


    content_panels = Page.content_panels + [
        #...
        FieldPanel('minAge'),
        FieldPanel('maxAge'),
        #..
    ]

    api_fields = [
        #...
        APIField('minAge'),
        APIField('maxAge'),
        #...
    ]

    search_fields = Page.search_fields + [
        #...
        index.FilterField('minAge'),
        index.FilterField('maxAge')
        #...
    ]
```

Now, once migrations have been ran, our services can both, add and be filtered by ages.

### Adding serviceTags and supportTypeTags

Tagging in Wagtail can be achieved using the taggit library, making use of the `ClusterTaggableManager`. Adding a `ClusterTaggableManager` to our Service page will allow for fields that represent an array of tags to be provided. Examples of how this is implemented can be found [here](https://docs.wagtail.io/en/stable/topics/snippets.html?highlight=tags#tagging-snippets).

To apply this to our Service pages, we would make the following changes:

```Python
## testSite/service/models.py

# Imports required for taggit
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class SupportTypeTag(TaggedItemBase):
    content_object = ParentalKey(
        'Service',
        related_name='support_type_tag',
        on_delete=models.CASCADE
    )

class ServiceTag(TaggedItemBase):
    content_object = ParentalKey(
        'Service',
        related_name='service_tag',
        on_delete=models.CASCADE
    )

class Service(Page):
    #existing variables, e.g. serviceId = models.CharField(max_length=100, unique=True)

    serviceTags = ClusterTaggableManager(through=ServiceTag, blank=True, related_name='serviceTags')
    supportTypeTags = ClusterTaggableManager(through=SupportTypeTag, blank=True, related_name='supportTypeTags')


    content_panels = Page.content_panels + [
        #...
        FieldPanel('serviceTags', heading="service tags"),
        FieldPanel('supportTypeTags', heading="support type tags"),
        #..
    ]

    api_fields = [
        #...
        APIField('serviceTags'),
        APIField('supportTypeTags'),
        #...
    ]

    search_fields = Page.search_fields + [
        #...
        index.FilterField('serviceTags'),
        index.FilterField('supportTypeTags'),
        #...
    ]
```

Now, once migrations have been ran, our services can both, add tags to a service, and also carry out exact filters.

---

## Adding a Custom Filter

### Current Issue

Ideally, the previous section should have sufficed and no further work would be required. Unfortunately, out of the box Wagtail had the following issues:

- minAge and maxAge will only provide direct comparison operators, so we can check that a value matches, but not that it's less than or greater than a value.
- Tags require matches to be exclusive, for example, `serviceTag=moodAndMotivation,anxiety` will only returns responses with only both moodAndMotivation and anxiety. We want this be an `OR` check, rather than an `AND` check.

Fortunately, we can extend filter functionality to allow for these cases. This will be explained in the following sections.

---

### Creating Service Filter

The first step is to create our custom filter, we will call this our `ServiceFilter`. All filters extend the `BaseFilterBackend` and need to implement the method `filter_queryset(self, request, queryset, view)`, which must return the `queryset`.

For this stage, we will create the bare minimum filter. First create `service/filters.py`, and then add the following code:

```Python
## testSite/service/filters.py

from rest_framework.filters import BaseFilterBackend

class ServiceFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset
```

### Service API Set

To implement our `ServiceFilter` and gain more control over the API, we will need to create our own APIViewSet, we will call this `ServiceAPISet`, and will keep the logic inside of `service/api.py`.

So far we have been using the `PagesAPIViewSet`, so we will extend this to ensure we keep as much of our current functionality as possible. To do this we will extend `PagesAPIViewSet`, and update the `filters_backend` value to include our new `ServiceFilter`.

This is achieved using the following code:

```Python
## testSite/service/api.py

from wagtail.api.v2.views import PagesAPIViewSet
from service.filters import ServiceFilter

class ServiceAPISet(PagesAPIViewSet):
    filter_backends = [ServiceFilter] + PagesAPIViewSet.filter_backends
```

Then we will tell our testSite to use our `ServiceAPISet` instead of `PagesAPISet` by updating our services endpoint in `testSite/api.py` like so:

```Python
# testSite/testSite/api.py

from wagtail.api.v2.router import WagtailAPIRouter
from service.api import ServiceAPISet

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

# The first parameter is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint('services', ServiceAPISet)

```

### Information about our planned usage

Now all calls the the `api/services` route will use our `ServiceAPISet`, we can implement our own logic on how filtering will work.

#### Ages logic

As [django QuerySet](https://docs.djangoproject.com/en/3.2/ref/models/querysets/) supports operators such as `lt`, `lte`, `gt` and `gte`, we would like to use these with fields (such as maxAge) to be able to use ages as we would like. To do this we will want to add suffixes to the values without our querystring. For example `maxAge__lte=15` should return all results where `maxAge <=15`.

#### Tags logic

We want our tags to operate using `ORs` rather than `ANDs`, e.g. `supportTypeTag=a,b` should return all services with either tags `a` or `b` (or both), not only those including both.

### Applying Logic to Service API Set

First, we need to consider that we will be basing our filter off of the `filter_queryset` method within `FieldsFilter`, due to this we should now remove the old `FieldsFilter` from our `ServiceAPISet`.

We will also need to consider that `PageApiViewSet` uses the ` check_query_parameters(self, queryset)` method to determine valid query parameters. This requires database values or specific exclusions only. To work around this for our age cases, we will want to also allow values which are database column names, suffixed with `__`. We can add this additional functionality by overwriting the `check_query_parameters` method inside of our `ServiceAPISet`.

In production, it would be a good idea to add additional checks to make sure the values after `__` are accepted types of [django field lookups](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups). In a similar way to how we check that the value before the `__` is in the database by checking against a frozen set (`allowed_query_parameters = set(self.get_available_fields(queryset.model, db_fields_only=True)).union(self.known_query_parameters)`), we want to create a new frozen set of all the accepted field lookup types `[gte, gt, lte, lt]` and check against this.

We can achieve all of this by making our `services/api.py` as following:

```Python
## testSite/service/api.py

from wagtail.api.v2.views import PagesAPIViewSet

from service.filters import ServiceFilter
from wagtail.api.v2.filters import (FieldsFilter)
from wagtail.api.v2.utils import BadRequestError

class ServiceAPISet(PagesAPIViewSet):
    filter_backends = [ServiceFilter] + PagesAPIViewSet.filter_backends
    filter_backends.remove(FieldsFilter) # Removes the old FieldsFilter from our API Set.

    ## This method simply returns values before '__' if present, e.g. maxAge__gte -> maxAge.
    def allow_underscore_values(self, value):
        if "__" in value:
            return value[:value.index("__")]
        return value

    def check_query_parameters(self, queryset):
        """
        Ensure that only valid query paramters are included in the URL.
        """
        request_keys = [self.allow_underscore_values(key) for key in self.request.GET.keys()]
        query_parameters = set(request_keys)

        # All query paramters must be either a database field or an operation
        allowed_query_parameters = set(self.get_available_fields(queryset.model, db_fields_only=True)).union(self.known_query_parameters)
        unknown_parameters = query_parameters - allowed_query_parameters
        if unknown_parameters:
            raise BadRequestError("query parameter is not an operation or a recognised field: %s" % ', '.join(sorted(unknown_parameters)))

```

### Applying Logic to Service Filter

Now that our `ServiceAPISet` class can accept the parameters as expected, we will want to add functionality to our `filter_queryset` method inside of `ServiceFilter` to handle query as we see fit, i.e. allowing for operators after `__` values to be processed, and allowing tag filters to work as an `OR` rather than an `AND` when being processed.

We have based our solution heavily from the original FieldsFilter. To see how this originally operated, please see the source code on [Github](https://github.com/wagtail/wagtail/blob/d58c90db5db443424a4c877f8010b0b8255e6770/wagtail/api/v2/filters.py#L14).

The following code shows how we achieved this.

```Python
# testSite/service/filters.py

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
```
