from wagtail.core import blocks
from django.db import models

from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import StructBlock
from wagtail.api import APIField
from wagtail.core import blocks
from wagtail.core.fields import StreamField

class CustomImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original").attrs_dict,
            }

class ImageCardBlock(StructBlock):
    label =  blocks.CharBlock(max=1024)
    image = CustomImageChooserBlock()


class ImageCardSteamField(StructBlock):
      image_cards = blocks.StreamBlock([
          ('image_card', ImageCardBlock())
      ], blank=True)
