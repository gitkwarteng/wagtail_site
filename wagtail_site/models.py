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
from wagtail.documents import get_document_model
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import DraftStateMixin, RevisionMixin, PreviewableMixin, TranslatableMixin, Orderable
from wagtail.models import Page

from .blocks import WebPageContentStreamBlock
from .choices import HeadingSizeChoices, ContentAlignmentChoices
from .mixins import PageEmailForm, DefaultTemplatesMixin


class AbstractWebPage(DefaultTemplatesMixin, ClusterableModel):

    base_template_name = 'wagtail_site/layout/base.html'

    web_template = None

    # banners = ParentalManyToManyField(
    #     'wagtail_site.WebPageBanner', blank=True, verbose_name="Banners"
    # )
    body = StreamField(
        [('body', WebPageContentStreamBlock())],
        blank=True
    )

    content_panels = Page.content_panels + [
        'banners',
        'body'
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

    def get_template(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.ajax_template or self.web_template or self.page_template
        else:
            return self.web_template or self.page_template



class AbstractFormWebPage(PageEmailForm, AbstractWebPage):

    form = models.ForeignKey('wagtail_site.PageForm', null=True, blank=True, verbose_name="Form", on_delete=models.SET_NULL,
                             related_name='+')

    form_panel = MultiFieldPanel([FormSubmissionsPanel(), FieldPanel('form'), ], "Page Form")

    content_panels = AbstractWebPage.content_panels + [
        form_panel
    ]

    class Meta:
        abstract = True


class WebPageBanner(Orderable):

    page = ParentalKey("wagtailcore.Page", on_delete=models.CASCADE, related_name='banners', null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL)
    heading = models.CharField(max_length=250, blank=True, null=True)
    content = RichTextField(blank=True, null=True, verbose_name="Description")
    size = models.CharField(
        max_length=5, blank=True, null=True,
        choices=HeadingSizeChoices.choices,
        default=HeadingSizeChoices.H1, verbose_name="Size"
    )
    position = models.CharField(
        max_length=5, blank=True, null=True,
        choices=ContentAlignmentChoices.choices,
        default=ContentAlignmentChoices.BOTTOM_LEFT, verbose_name="Position"
    )

    button_label = models.CharField(
        verbose_name="Button Label", max_length=250, blank=True, null=True)
    button_link = models.ForeignKey(
        Page, verbose_name="Button Link", blank=True, null=True, on_delete=models.SET_NULL,
        related_name='banner_button'
    )

    panels = [
        FieldRowPanel(
            [
                'name',
                'heading',
            ]
        ),

        FieldRowPanel([
            'size',
            'position',
        ]),

        FieldRowPanel([
            'button_label',
            'button_link'
        ]),

        'content',
        'image',
    ]

    def __str__(self):
        return f'{self.name or ""} {self.image.title}'


class TeamMember(Orderable):

    name = models.CharField("Name", max_length=50)
    image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL)
    profile = RichTextField("Profile", blank=True, null=True)

    link = models.URLField("URL", max_length=255, blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    @property
    def image_url(self):
        return self.image.url if self.image else ''


class Review(TranslatableMixin, DraftStateMixin, RevisionMixin, Orderable):

    name = models.CharField("Name", max_length=250)
    role = models.CharField("Role", max_length=250, blank=True, null=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL)
    content = RichTextField("Content", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ('translation_key', 'locale')



class WebPage(AbstractFormWebPage, Page):

    content_panels = Page.content_panels + [
        'banners',
        'team_members',
        'page_reviews',
        'form',
        'body'
    ]

    class Meta:
        verbose_name = "Web Page"
        verbose_name_plural = "Web Pages"


class WebPageTeamMember(Orderable):
    page = ParentalKey('wagtail_site.WebPage', related_name='team_members')
    team_member = models.ForeignKey('wagtail_site.TeamMember', related_name='+', on_delete=models.CASCADE)


class WebPageReview(Orderable):
    page = ParentalKey('wagtail_site.WebPage', related_name='page_reviews')
    review = models.ForeignKey('wagtail_site.Review', related_name='+', on_delete=models.CASCADE)


class DocumentsPage(AbstractWebPage):
    documents = StreamField([
        ('document', DocumentChooserBlock())
    ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        'banners',
        'documents',
        'body',
    ]

    class Meta:
        abstract = True


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
    footer_logo = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    linkedin = models.URLField(verbose_name="LinkedIn URL", blank=True)
    github = models.URLField(verbose_name="GitHub URL", blank=True)
    discord = models.URLField(verbose_name="Discord URL", blank=True)
    twitter = models.URLField(verbose_name="Twitter URL", blank=True)
    facebook = models.URLField(verbose_name="Facebook URL", blank=True)
    instagram = models.URLField(verbose_name="Instagram URL", blank=True)
    youtube = models.URLField(verbose_name="Youtube URL", blank=True)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=100)
    address = RichTextField(blank=True, null=True, max_length=250)
    map = models.CharField(blank=True, null=True, max_length=250, verbose_name="Google Maps Address")

    select_related = [
        'logo',
        'logo_landscape',
        'footer_logo',
    ]

    panels = [
        'logo',
        'logo_landscape',
        'footer_logo',
        'footer_text',

        MultiFieldPanel(
            [
                "linkedin",
                "github",
                "twitter",
                "discord",
                "facebook",
                "instagram",
                "youtube",
            ],
            "Social settings",
        ),

        MultiFieldPanel(
            [
                "phone",
                "email",
                "address",
                "map"
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
