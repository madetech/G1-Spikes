# Disabling Free Tagging in Wagtail

More information on this topic can be found [here](https://docs.wagtail.io/en/stable/reference/pages/model_recipes.html#disabling-free-tagging).

An example of this within our own code could be as follows (using location as an example):

```Python
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.api import APIField
from wagtail.search import index

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import ItemBase, TagBase
from wagtail.snippets.models import register_snippet

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
    #...

    locationTags = ClusterTaggableManager(through='service.TaggedLocation', blank=True)

    content_panels = Page.content_panels + [
        #...
        FieldPanel('locationTags', heading="location tags"),
    ]

    api_fields = [
        # ...
        APIField('locationTags')
    ]

    search_fields = Page.search_fields + [
        #...
        index.FilterField('locationTags')
    ]
```

The admin UI will now display a `snippets` section. This section will allow for tags to be created. Only Tags created there can be used within the location field.
