# from wagtail.api.v2.views import PagesAPIViewSet
# from wagtail.api.v2.router import WagtailAPIRouter
# from wagtail.images.api.v2.views import ImagesAPIViewSet
# from wagtail.documents.api.v2.views import DocumentsAPIViewSet
# # Create the router. "wagtailapi" is the URL namespace
# api_router = WagtailAPIRouter('wagtailapi')

# from django.urls import path

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endppagesoint class that handles the requests

# class ServicesAPIEndpoint(PagesAPIViewSet):
    
    # def hello(self, request):
    #     print('hello')
    
    # @classmethod
    # def get_urlpatterns(cls):
    #     return [
    #         path('', cls.as_view({'get': 'listing_view'}), name='listing'),
    #         path('service/', cls.as_view({}))
    #         path('<int:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
    #         path('find/', cls.as_view({'get': 'find_view'}), name='find'),
    #     ]

from wagtail.api.v2.router import WagtailAPIRouter
from service.api import ServiceAPISet

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', ServiceAPISet)