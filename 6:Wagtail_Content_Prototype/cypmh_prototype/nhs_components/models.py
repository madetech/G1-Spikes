from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.api import APIField
from wagtail.core import blocks

from wagtailnhsukfrontend.blocks import ActionLinkBlock, WarningCalloutBlock,InsetTextBlock, CareCardBlock, DetailsBlock
from .blocks import CustomImageBlock, CustomCareCardBlock
class NHSPage(Page):
  body = StreamField([
      # Include any of the blocks you want to use.
      ('action_link', ActionLinkBlock()),
      ('callout', WarningCalloutBlock()),
      ('heading', blocks.CharBlock(form_classname="heading")),
      ('inset_text', InsetTextBlock()),
      ('care_card', CustomCareCardBlock()),
      ('details', DetailsBlock()),
      ('text_content', blocks.RichTextBlock(features=['h2','h3','bold','italic','ul','ol','link'])),
      ('image', CustomImageBlock())
  ])

  content_panels = Page.content_panels + [
      StreamFieldPanel('body'),
  ]

  api_fields = [
      APIField('body'),
  ]