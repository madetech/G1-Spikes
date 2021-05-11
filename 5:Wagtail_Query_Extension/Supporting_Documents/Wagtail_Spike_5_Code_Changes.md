# Wagtail Code Changes

This document addressed the changes made to the Wagtail files. The pre-requisits for this can be found in the supporting_documents for the [first spike](../../1:Content_Query_and_Filtering/Content_Query_and_Filtering_Report.md) and the [second spike](../../2:Wagtail_Infrastructure_Requirements/Wagtail_Infrastructure_Requirements_Report.md).

## Service Model Changes

The first notable change made to the code will be found within our services model (`service/models.py`). Here we make 2 major changes, the introduction of `minAge` and `maxAge`, as well as the introduction of `serviceTags` and `supportTypeTags` using ClusterTaggableManager.

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

Now, once migrations have been ran, our services can both add and be filtered by ages.

## Creating Service Filter

## Service API Set

## Applying Logic to Service Filter

1. Model changes (i.e. tags and numbers)
2. Creating service Filter
3. PageViewAPI
4. Logic behind Service filter
