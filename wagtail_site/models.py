from functools import cached_property

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,

    PublishingPanel, InlinePanel, FieldRowPanel
)
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm, EmailFormMixin

from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import DraftStateMixin, RevisionMixin, PreviewableMixin, TranslatableMixin, Orderable
from wagtail.models import Page

from .blocks import WebPageContentStreamBlock
from .choices import HeadingSizeChoices, ContentAlignmentChoices
from .mixins import PageEmailForm


class AbstractWebPage(models.Model):

    base_template_name = 'wagtail_site/layout/base.html'

    intro = RichTextField(blank=True, null=True)
    banner = models.ForeignKey('wagtail_site.WebPageBanner', null=True, blank=True, verbose_name="Banner", on_delete=models.SET_NULL,
                               related_name='+')
    body = StreamField(
        [('body', WebPageContentStreamBlock())],
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner'),
        FieldPanel('body')
    ]

    class Meta:
        abstract = True

    @cached_property
    def current_site(self):
        return self.get_site()

    def get_base_template(self, *args, **kwargs):
        return self.base_template_name

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['wagtail_site_base'] = self.get_base_template()

        return context


class AbstractFormWebPage(PageEmailForm, AbstractWebPage):

    form = models.ForeignKey('wagtail_site.PageForm', null=True, blank=True, verbose_name="Form", on_delete=models.SET_NULL,
                             related_name='+')

    content_panels = AbstractWebPage.content_panels + [

        MultiFieldPanel([

            FormSubmissionsPanel(),

            FieldPanel('form'),

        ], "Page Form")

    ]

    class Meta:
        abstract = True


class HomePage(AbstractWebPage):
    pass


class WebPageBanner(models.Model):

    image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL)
    caption = models.CharField(max_length=250, blank=True, null=True)
    caption_size = models.CharField(max_length=5, blank=True, null=True,
                                    choices=HeadingSizeChoices.choices,
                                    default=HeadingSizeChoices.H1, verbose_name="Size")
    caption_position = models.CharField(max_length=5, blank=True, null=True,
                                        choices=ContentAlignmentChoices.choices,
                                        default=ContentAlignmentChoices.BOTTOM_LEFT, verbose_name="Position")

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
        FieldPanel('caption_size'),
        FieldPanel('caption_position'),
    ]

    def __str__(self):
        return f'{self.image.title} - {self.caption}'


class FormField(AbstractFormField):

    def __str__(self):
        return f'{self.label}'


class PageForm(EmailFormMixin, ClusterableModel, Orderable):

    name = models.CharField(max_length=250, blank=True, null=True)

    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [

        FieldPanel('name'),

        FieldPanel('thank_you_text'),

        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),

        ], "Email Details"),

        InlinePanel('fields', label="Form fields"),
    ]

    panels = [
        'name', 'thank_you_text', 'from_address', 'to_address', 'subject', 'fields',
    ]

    def __str__(self):
        return f'{self.name}'


class PageFormField(Orderable):
    form = ParentalKey('wagtail_site.PageForm', on_delete=models.CASCADE, related_name='fields')
    field = models.ForeignKey(
        'FormField', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('field')
    ]

    clean_name = None

    def get_field_clean_name(self):
        return self.field.clean_name or self.field.get_field_clean_name()


@register_setting
class SiteSettings(BaseGenericSetting):
    footer_text = RichTextField()
    logo = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    logo_landscape = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    linkedin = models.URLField(verbose_name="LinkedIn URL", blank=True)
    github = models.URLField(verbose_name="GitHub URL", blank=True)
    discord = models.URLField(verbose_name="Discord URL", blank=True)
    twitter = models.URLField(verbose_name="Twitter URL", blank=True)
    facebook = models.URLField(verbose_name="Facebook URL", blank=True)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=100)
    address = RichTextField(blank=True, null=True, max_length=250)

    select_related = [
        'logo',
        'logo_landscape',
    ]

    panels = [
        FieldPanel('logo'),
        FieldPanel('logo_landscape'),
        FieldPanel('footer_text'),

        MultiFieldPanel(
            [
                FieldPanel("linkedin"),
                FieldPanel("github"),
                FieldPanel("twitter"),
                FieldPanel("discord"),
                FieldPanel("facebook"),
            ],
            "Social settings",
        ),

        MultiFieldPanel(
            [
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("address")
            ],
            "Contact settings",
        )
    ]


class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"
