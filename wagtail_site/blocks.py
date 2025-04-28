from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock

from .choices import ContentAlignmentChoices, HeadingSizeChoices, ContentDirectionChoices


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
        default=ContentAlignmentChoices.LEFT
    )

    class Meta:
        icon = "title"
        template = "blocks/heading-block.html"

class CaptionedImageBlock(blocks.StructBlock):
    image = ImageBlock(required=False)
    caption = blocks.CharBlock(required=False)
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/captioned-image-block.html"


class WebPageContentStreamBlock(blocks.StructBlock):
    icon = blocks.TextBlock(required=False)
    heading = WebPageHeadingBlock(required=False)
    content = blocks.RichTextBlock(required=False)
    image = CaptionedImageBlock(required=False)
    direction = blocks.ChoiceBlock(
        choices=ContentDirectionChoices.choices, default=ContentDirectionChoices.LEFT_TO_RIGHT,
        help_text="Direction of the content. Left to right means text is displayed on the left and image on the right."
    )

    class Meta:
        icon = "image"
        template = "blocks/content-block.html"

