from wagtail.api.v2.views import PagesAPIViewSet

from service.filters import ServiceFilter
from wagtail.api.v2.filters import (FieldsFilter)

class ServiceAPISet(PagesAPIViewSet):
    filter_backends = [ServiceFilter] + PagesAPIViewSet.filter_backends
    filter_backends.remove(FieldsFilter)