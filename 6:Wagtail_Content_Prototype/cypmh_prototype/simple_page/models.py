from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.api import APIField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock


class SimplePage(Page):
  content = RichTextField()
  steam_field_content = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        
    ], blank=True)

  content_panels = Page.content_panels + [
        FieldPanel('content'),
        StreamFieldPanel('steam_field_content')
    ]

  api_fields = [
              APIField('content'),
              APIField('steam_field_content')

          ]

  # search_fields = Page.search_fields + [
  #   index.SearchField('url_path'),
  #   index.FilterField('url_path'),
  # ]