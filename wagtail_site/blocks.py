from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock

from .choices import ContentAlignmentChoices, HeadingSizeChoices


class CarousalStreamBlock(blocks.StreamBlock):
    image = ImageBlock(required=False)
    video = EmbedBlock(required=False)
    caption = blocks.CharBlock(required=False)


class WebPageHeadingBlock(blocks.StructBlock):
    title = blocks.CharBlock(classname="title")
    subtitle = blocks.CharBlock(required=False)

    size = blocks.ChoiceBlock(
        choices=HeadingSizeChoices.choices
    )
    position = blocks.ChoiceBlock(
        choices=ContentAlignmentChoices.choices,
        default=ContentAlignmentChoices.BOTTOM_LEFT
    )

    class Meta:
        icon = "title"
        # template = "base/blocks/heading_block.html"

class CaptionedImageBlock(blocks.StructBlock):
    image = ImageBlock(required=False)
    caption = blocks.CharBlock(required=False)
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        # template = "base/blocks/captioned_image_block.html"


class WebPageContentStreamBlock(blocks.StructBlock):
    icon = blocks.TextBlock(required=False)
    heading = WebPageHeadingBlock(required=False)
    content = blocks.RichTextBlock(required=False)
    image = CaptionedImageBlock(required=False)
    alignment = blocks.ChoiceBlock(choices=ContentAlignmentChoices.choices, default=ContentAlignmentChoices.LEFT)
