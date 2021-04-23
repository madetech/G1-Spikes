# Content Query and Filtering

<!-- What the Task was, intro, etc.  -->

## Setting up Wagtail for Spike
<!--  Pulling down and Setup; Setting the Query Fields (e.g. Search Field, and Filter Field) -->
### Prerequisite
We must first create a wagtail instance and expose the API. To do this we follow these two documents in order:
1. [Set up a local wagtail instance](./Supporting_Documents/Set_Up_A_Local_Wagtail_Instance.md).
2. [Enable Wagtail API ](./Supporting_Documents/Enable_Wagtail_API.md).

### Creating the service application
First we will need to create a service application that our content can rely on. To do this, we complete the following from our virtual environment.
1. Create a new service by running `python3 manage.py startapp service` at the root level, this should create a application directory called `service`.
2. Add the new application to `INSTALLED_APPS` inside of the main site settings, so for a website called `wagtailspikes`, this would be `wagtailspikes/settings.base.py`, and values are added to the array like to:
    ```python
    # Application definition

    INSTALLED_APPS = [
        'home',
        'search',
        'blog',
        'service',

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

### Create our Service Model and Page
Next, we will need to create a model and page that can be used by CMS users to add services. It should be noted that even though we are headless and will not create a frontend template, we will still use the concept of "Pages" as where our services are stored.
1. Create the models file inside of the service application e.g. `service/models.py`.
2. Add the following code to `service/models.py`:
    ```python
    from django.db import models

    from wagtail.core.models import Page
    from wagtail.admin.edit_handlers import FieldPanel

    class Service(Page):
        serviceId = models.CharField(max_length=100, unique=True)

        # OR test case
        name = models.CharField(max_length=100)
        
        # And test case
        supportType = models.CharField(max_length=100)
        

        content_panels = Page.content_panels + [
            FieldPanel('serviceId'),
            FieldPanel('name'),
            FieldPanel('supportType'),
        ]

    ```

3. Run the appropriate migrations using the following:
    ```console
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
4. Verify this has worked by going to the admin panel, and moving to add a page, a service page should now be availble to add, allowing an serviceId, name and supportType to be added.

### Allowing our fields to be returned via the API
If we attempt to query the API for our new services, our values will not return, only those that are defaults of page. This is because we will need to explicitly state that they should return. To do this we add the following to our `Service` class.
```python
        from wagtail.api import APIField
        
        ...
        
        class Service(Page):

            ...

            api_fields = [
                APIField('serviceId'),
                APIField('name'),
                APIField('supportType'),
            ]
```
This will state that any value specified in that array can be returned by the API. **This does not mean that they always will be**.<br />
To ensure ensure that these are returned we must use the type and fields values within our query: <br />
- `type` - the page type we want to return.
- `fields` - the fields which should be returned.

In our case `type` will always be `service.Service`, for fields we can inivudally state fields e.g. `fields=serviceId,name,supportType`, or we can simply use the wildcard `*`, to return all fields.

To test this, the following query `localhost:8000/api/pages/?type=service.Service&fields=*`, should return all service pages with all fields.

## Allowing for Searching and Filter by Our Types
Finally, we need to be able to search and filter by our types, to do this we simply need to add to the `search_fields` array, much like we did with the api_fields. Within the `models.py` add the following:
```python
    from wagtail.search import index


    search_fields = Page.search_fields + [
        index.SearchField('serviceId'),
        index.SearchField('name'),
        index.FilterField('name'),
        index.SearchField('supportType'),
        index.FilterField('supportType'),
```
This will allow for us to Search (`search=`) on `serviceId`,`name`, and `supportType`, and filter by `name` (`name=`) and `supportType` (`supportType=`).
## What we Tested and Results
<!--  What Queries we tried (the 4 test cases, and results) -->

## Issues
<!--  Test case 4 is not working, and multiple AND filters seems to be a pain, seems like multiple ands are not supported out of the BOX  -->

## Suggestions
<!-- Maybe use graphql, Q langauge, etc. return everything and Serverside Filter in React,  -->

