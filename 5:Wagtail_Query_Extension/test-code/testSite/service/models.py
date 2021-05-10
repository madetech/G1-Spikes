from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.api import APIField
from wagtail.search import index
from wagtail.core.fields import RichTextField


from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# from service.filters import ServiceFilter

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
    serviceId = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = RichTextField()
    maxAge = models.IntegerField()
    minAge = models.IntegerField()
    #url = models.URLField()
    serviceTags = ClusterTaggableManager(through=ServiceTag, blank=True, related_name='serviceTags')
    supportTypeTags = ClusterTaggableManager(through=SupportTypeTag, blank=True, related_name='supportTypeTags')

    
    content_panels = Page.content_panels + [
        FieldPanel('serviceId'),
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        FieldPanel('minAge'),
        FieldPanel('maxAge'),
        FieldPanel('serviceTags', heading="test"),
        FieldPanel('supportTypeTags', heading="anotherTests")
        # FieldPanel('url'),
        # MultiFieldPanel([
        #     FieldPanel('tags'),
        # ], heading="Relevant Tags"),

    ]
    api_fields = [
                APIField('serviceId'),
                APIField('name'),
                APIField('description'),
                APIField('minAge'),
                APIField('maxAge'),
                APIField('serviceTags'),
                APIField('supportTypeTags'),
            ]

    search_fields = Page.search_fields + [
        index.SearchField('serviceId'),
        index.FilterField('serviceId'),
        index.SearchField('name'),
        index.SearchField('description'),
        index.FilterField('name'),
        index.SearchField('maxAge'),
        index.SearchField('minAge'),
        index.FilterField('serviceTags')
        # index.FilterField('maxAge'),
        # index.FilterField('minAge'),
        # index.RelatedFields('serviceTags', [
        #         index.SearchField('name', partial_match=True, boost=10),
        #     ]),
        # index.RelatedFields('tags', [
        #     index.SearchField('supportTypeTags', partial_match=True, boost=10),
        # ]),

    ]
