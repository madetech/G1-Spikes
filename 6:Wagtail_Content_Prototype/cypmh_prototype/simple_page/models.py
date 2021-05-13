from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.api import APIField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock

from .blocks import ImageCardBlock, ImageCardSteamField 

class SimplePage(Page):
  page_content = StreamField([
        ('sub_heading', blocks.CharBlock(form_classname="Sub-Heading")),
        ('paragraph', blocks.CharBlock()),
        ('image_cards', ImageCardSteamField()),
    ], blank=True)

  content_panels = Page.content_panels + [
      StreamFieldPanel('page_content'),
    ]

  api_fields = [
    APIField('page_content')
  ]
