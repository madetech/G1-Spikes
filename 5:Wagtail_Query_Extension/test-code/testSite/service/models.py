from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.api import APIField
from wagtail.search import index
from wagtail.core.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, ItemBase, TagBase
from wagtail.snippets.models import register_snippet

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


@register_snippet
class LocationTag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "Location tag"
        verbose_name_plural = "Location tags"


class TaggedLocation(ItemBase):
    tag = models.ForeignKey(
        LocationTag, related_name="tagged_locations", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to='service.Service',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )

class Service(Page):
    serviceId = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = RichTextField()
    maxAge = models.IntegerField()
    minAge = models.IntegerField()
    serviceTags = ClusterTaggableManager(through=ServiceTag, blank=True, related_name='serviceTags')
    supportTypeTags = ClusterTaggableManager(through=SupportTypeTag, blank=True, related_name='supportTypeTags')
    locationTags = ClusterTaggableManager(through='service.TaggedLocation', blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('serviceId'),
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        FieldPanel('minAge'),
        FieldPanel('maxAge'),
        FieldPanel('serviceTags', heading="service tags"),
        FieldPanel('supportTypeTags', heading="support type tags"),
        FieldPanel('locationTags', heading="location tags")
    ]
    api_fields = [
                APIField('serviceId'),
                APIField('name'),
                APIField('description'),
                APIField('minAge'),
                APIField('maxAge'),
                APIField('serviceTags'),
                APIField('supportTypeTags'),
                APIField('locationTags')
            ]

    search_fields = Page.search_fields + [
        index.SearchField('serviceId'),
        index.FilterField('serviceId'),
        index.SearchField('name'),
        index.SearchField('description'),
        index.FilterField('name'),
        index.FilterField('minAge'),
        index.FilterField('serviceTags'),
        index.FilterField('supportTypeTags'),
        index.FilterField('maxAge'),
        index.FilterField('locationTags')
    ]
