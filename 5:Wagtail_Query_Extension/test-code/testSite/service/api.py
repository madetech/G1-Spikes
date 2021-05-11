from wagtail.api.v2.views import PagesAPIViewSet

from service.filters import ServiceFilter
from wagtail.api.v2.filters import (FieldsFilter)
from wagtail.api.v2.utils import BadRequestError
class ServiceAPISet(PagesAPIViewSet):
    filter_backends = [ServiceFilter] + PagesAPIViewSet.filter_backends
    filter_backends.remove(FieldsFilter)

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