# Content Query and Filtering
Investigate whether and how Wagtail provides the querying and filtering functionality that will be required to retrieve services and other content types by criteria. More information can be found in [ticket](https://trello.com/c/yOESxJGo/44-wagtail-content-query-filtering-capability).

## Setting up Wagtail for Spike
### Prerequisite
We must first create a wagtail instance and expose the API. To do this we follow these two documents in order:
1. [Set up a local wagtail instance](./Supporting_Documents/Set_Up_A_Local_Wagtail_Instance.md).
2. [Enable Wagtail API ](./Supporting_Documents/Enable_Wagtail_API.md).

### Creating the service application
First we will need to create a service application that our content can rely on. To do this, we complete the following from our virtual environment.
1. Create a new service by running `python3 manage.py startapp service` at the root level, this should create a application directory called `service`.
2. Add the new application to `INSTALLED_APPS` inside of the main site settings, so for a website called `wagtailspikes`, this would be `wagtailspikes/settings.base.py`, and values are added to the array:
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
Given that the CYMPH Site will require filtering specific services, we tested how this could be performed in Wagtail. 

Services could be a list of OR'd services, e.g. Groups of Concerns. Services may also be filtered by specific conditions - for example Support type. 

Lists of Services need to be OR'd and a one to many relationship. Specific conditions need to be used to only return those services that match a specifc use case, e.g Services that have Helpline support. 

We tried the following test combinations to see how Wagtail's out of the box search function worked, and what would be returned:

1. Simple OR Case:

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" 
```

Expected test result: expect both services returned

Result: <span style="color:green">PASS</span>

2. Simple OR Case, filtered with one AND:

```bash
 "Mood and Motivation" OR "Feeling worried and Anxious" AND "Counselling"
 ```

Expected test result:  expect both services returned

Result: <span style="color:green">PASS</span>

3. Three OR's filtered with one AND:

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" 
```

Expected test result: expect ONLY Eating habits or body image returned

Result: <span style="color:green">PASS</span>

4. Three OR's filtered with two AND's (which are OR'd):

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" OR "Counselling" 
```

Expected test result: Expect all services back

Result: <span style="color:crimson">FAIL</span>

## Issues
The way Wagtail appears to oppertate out of the box, is to allow either multiple AND's filtered by a single OR - or - for multiple OR's to be filtered by a single AND. 

We tried a few different ways of getting condition 4 to pass, but were unsucessful. 

## Suggestions
Since Wagtail is based on Django we could extend some of the search functionality to meet our needs. Possible ways of doing this are listed below:

<!-- wagtail-->
1. ### Use GraphQL.
    A [GraphQL plugin](https://wagtail.io/blog/getting-started-with-wagtail-and-graphql/) has been found that we could potentially use. Whilst more investigation would be needed, however conceptually this could be a solution.  



    #### Pros
    + Established technology.
    + Seems to be good use case for GraphQL.
    #### Cons
    - Requires custom extension.
    - Will require changes to NextJs backend functionality.
    - Will require knowledge/investigation of how GraphQL works.

2. ### Use Q language to extend current Search functionality
    As this is Django based, we could creat our own custom search and filter components that make use of Q language. 

    #### Pros
    + Established technology.
    + Python based and built-in to Django.
    #### Cons
    - Requires investigation into creating custom search/filter functions and classes.
    - Will require more in-depth Django and data querying expertise.
    - Will need confirmation if this compliments or replaces Wagtail's search functionallity.

3. ### Single large request that we filter.
    A simple work around where we get all servies and do all filtering and sorting on the Nextjs backend.

    #### Pros
    + Quickest method.

    #### Cons
    - Heavier lifting for the backend.
    - Wagtail now only serves requests, we don't take advantage of the in-built features.

4. ### Multiple http requests from the NextJs backend.
    A simple work around would be to call the API multiple times, once for each filter.

    #### Pros
    + Quick to set-up.
    #### Cons
    - Multiple calls, so we need to consider throttling and network drops.
    - We need to extend current functionality to allow us to merge and filter results.
    - The number of calls is directly related to the number of filters selected.

5. ### Using a lambda to map between NextJs and Wagtail API.
    Finally, we could also use a lambda to map between the two methods, this copies the multiple HTTP request method, but prevents any changes to be needed to the NextJs backend. 

    #### Pros
    + No changes needed to NextJs.
    + Could be swapped in and out easily.
    + Provides seperation between NextJs and Wagtail.

    #### Cons
    - Longest to set-up
    - Requires infrastructure changes.
    - Most expensive.
    - Adds another managed service.

6. ### Allowing the NextJs app to use DynamoDB for Services, and use a Lambda to push Wagtail content to DynamoDB
    A team discussion revealed that we could still make use of DynamoDB. Unfortunatley it does not appear that wagtail has a simple plug-and-play option for Dynamo; however, we can create a Lambda to synch Dynamo with the Wagtail database.

    ### Pros
    + We get to keep current infrastructure, prevent a tech debt build up.
    + No need for multiple Wagtail calls per lookup for Services.
    + Client wouldn't notice any difference regarding where the content is served from, and still be able to maintain Service content in Wagtail.
    + Removing known unknowns, avoiding extra investigation into how to extend Wagtail to use Q language or GraphQL

    ### Cons
    - Could be extra expense (DynamoDB, Lambda (although minimal))
    - More maintenence/infraastrucure 
    - Data inconsistency could exist if the Lambda fails, leading to different information stored in Wagtail vs. in DynamoDB

## Preferred Solution
After discussing with the team we think that Option 6 would be the preferred option. It should be failry straightforward to use a Databae Hook which monitor