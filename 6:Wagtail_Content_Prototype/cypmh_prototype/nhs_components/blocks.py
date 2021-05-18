from wagtailnhsukfrontend.blocks import ImageBlock, CareCardBlock
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
  #     richtext = RichTextBlock()
  #     action_link = ActionLinkBlock()
  #     details = DetailsBlock()
  #     inset_text = InsetTextBlock()
      image = CustomImageBlock()
  #     grey_panel = GreyPanelBlock()
  #     feature_card = CardFeatureBlock()
  #     warning_callout = WarningCalloutBlock()
  #     summary_list = SummaryListBlock()

  body = CustomBodyStreamBlock(required=True)