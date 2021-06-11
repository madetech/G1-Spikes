from wagtailnhsukfrontend.blocks import ImageBlock, CareCardBlock, CardGroupBlock, CardImageBlock
from wagtail.core.blocks import StreamBlock
from wagtail.images.blocks import ImageChooserBlock

class CustomImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original").attrs_dict,
            }

class CustomImageBlock(ImageBlock):
  content_image = CustomImageChooserBlock()


class CustomCareCardBlock(CareCardBlock):

  class CustomBodyStreamBlock(CareCardBlock.BodyStreamBlock):
      image = CustomImageBlock()


  body = CustomBodyStreamBlock(required=True)

class CustomCardImageBlock(CardImageBlock):
    content_image = CustomImageChooserBlock(label='Image', required=True)
  
class CustomCardGroupBlock(CardGroupBlock):
    class CustomBodyStreamBlock(CardGroupBlock.BodyStreamBlock):
        card_image = CustomCardImageBlock()


    body = CustomBodyStreamBlock(required=True)
