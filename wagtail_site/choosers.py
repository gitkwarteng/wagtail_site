from wagtail.admin.panels import FieldPanel
from wagtail.admin.viewsets.chooser import ChooserViewSet


class PageBannerChooserViewSet(ChooserViewSet):

    model = "wagtail_site.WebPageBanner"

    icon = "image"
    choose_one_text = "Choose a banner"
    choose_another_text = "Choose another banner"
    edit_item_text = "Edit this banner"
    form_fields = ["image", "caption", 'caption_size', 'caption_position']  # fields to show in the "Create" tab

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("caption_size"),
        FieldPanel("caption_position"),
    ]

banner_chooser_viewset = PageBannerChooserViewSet("banner_chooser")


class FormFieldChooserViewSet(ChooserViewSet):

    model = "wagtail_site.FormField"

    icon = "pilcrow"
    choose_one_text = "Choose a field"
    choose_another_text = "Choose another field"
    edit_item_text = "Edit this field"
    form_fields = ['label', 'field_type', 'required', 'choices', 'default_value', 'help_text']

    panels = [
        FieldPanel("label"),
        FieldPanel("field_type"),
        FieldPanel("required"),
        FieldPanel("choices"),
        FieldPanel("default_value"),
        FieldPanel("help_text"),
    ]

form_field_chooser_viewset = FormFieldChooserViewSet("field_chooser")


class FormChooserViewSet(ChooserViewSet):

    model = "wagtail_site.PageForm"

    icon = "pilcrow"
    choose_one_text = "Choose a form"
    choose_another_text = "Choose another form"
    edit_item_text = "Edit this form"
    form_fields = ['name', 'from_address', 'to_address', 'subject', 'thank_you_text']

    panels = [
        'name', 'from_address', 'to_address', 'subject', 'thank_you_text', 'fields'
    ]

page_form_chooser_viewset = FormChooserViewSet("form_chooser")