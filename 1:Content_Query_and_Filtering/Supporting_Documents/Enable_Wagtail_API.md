# Enable Wagtail API
This is a short and concise tutorial on how we allow our wagtail instance to be accessed via an API, returning information held by Wagtail. More information on this can be found in the [official documentation](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/configuration.html).

## Prerequisite
We assume that a local wagtail instance has already been created. 
If an instance is not already set-up, please follow the [Set Up a Local Wagtail Instance](./Set_Up_A_Local_Wagtail_Instance.md) document.

## Exposing The Wagtail API
1. The first step in exposing the API is to enable the Wagtail API app. To do this, first go to your projects base settings, so for a project called "wagtailspikes" this would be, `wagtailspikes/settings/base.py`. Then add `'wagtail.api.v2',` to the INSALLED_APPS array, as such:
   ```python
   # Application definition

    INSTALLED_APPS = [
        'home',
        'search',
        'blog',

        'wagtail.contrib.forms',
        'wagtail.contrib.redirects',
        'wagtail.embeds',
        'wagtail.sites',
        'wagtail.users',
        'wagtail.snippets',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.search',
        'wagtail.admin',
        'wagtail.core',

        'wagtail.api.v2',
    ]
   ```
    _You can also enable `rest_framework` if planning to debug using the browser._

2. Configure the endpoints, providing the paths and Endpoint classes. To do this for the 3 main content types (pages, images, and documents), we would first create an api.py within our project (`wagtailspieks/api.py`), then add the following code:
    ```python
    from wagtail.api.v2.views import PagesAPIViewSet
    from wagtail.api.v2.router import WagtailAPIRouter
    from wagtail.images.api.v2.views import ImagesAPIViewSet
    from wagtail.documents.api.v2.views import DocumentsAPIViewSet

    # Create the router. "wagtailapi" is the URL namespace
    api_router = WagtailAPIRouter('wagtailapi')

    # Add the three endpoints using the "register_endpoint" method.
    # The first parameter is the name of the endpoint (eg. pages, images). This
    # is used in the URL of the endpoint
    # The second parameter is the endpoint class that handles the requests
    api_router.register_endpoint('pages', PagesAPIViewSet)
    api_router.register_endpoint('images', ImagesAPIViewSet)
    api_router.register_endpoint('documents', DocumentsAPIViewSet)
    ```
3. Next we need to register the URLs to allow Django to route the requests. This is done by adding the paht and urls to `urls.py`, e.g.
    ```python
    from .api import api_router

    urlpatterns = [
        path('api/v2/', api_router.urls),
        ...
    ]
    ```
4.  Finally to verify everything is set-up correctly, make a request to http://localhost:8000/api/pages/ . This should return a JSON object containing information about all pages.