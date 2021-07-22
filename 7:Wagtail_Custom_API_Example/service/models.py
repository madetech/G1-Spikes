from django.db import models

from taggit.models import TaggedItemBase

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.api import APIField
from wagtail.search import index
from wagtail.search.utils import OR

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from taggit.models import Tag

from pprint import pprint

class ServiceTag(TaggedItemBase):
    content_object = ParentalKey(
        'Service',
        related_name='serviceTag',
        on_delete=models.CASCADE
    )


class Service(Page):
    serviceId = models.CharField(max_length=100, unique=True)
    description = RichTextField(blank=True)
    maxAge = models.PositiveIntegerField(default=100)
    minAge = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    serviceUrl = models.URLField()
    tags = ClusterTaggableManager(through=ServiceTag, blank=True)
    
    extra_search = {'operator': OR}
    
    #And
    supportType = models.CharField(max_length=100)
    

    content_panels = Page.content_panels + [
        FieldPanel('serviceId'),
        FieldPanel('description'),
        FieldPanel('maxAge'),
        FieldPanel('minAge'),
        FieldPanel('name'),
        FieldPanel('serviceUrl'),
        FieldPanel('supportType'),
        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="tags"),
    ]
    
    api_fields = [
        APIField('serviceId'),
        APIField('description'),
        APIField('maxAge'),
        APIField('minAge'),
        APIField('name'),
        APIField('serviceUrl'),
        APIField('supportType'),
        APIField('tags'),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('serviceId'),
        index.SearchField('description'),
        index.SearchField('maxAge'),
        index.SearchField('minAge'),
        index.SearchField('name'),
        index.SearchField('serviceUrl'),
        index.FilterField('maxAge'),
        index.FilterField('name'),
        index.FilterField('supportType'),
    ]
    
    pprint('')

# class SupportTypeField(BaseField):
    