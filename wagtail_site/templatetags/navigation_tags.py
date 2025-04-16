from django import template
from django.conf import settings
from django.apps import apps
from wagtail.models import Site

from wagtail_site.models import FooterText

register = template.Library()


@register.inclusion_tag("common/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }


@register.simple_tag(takes_context=True)
def get_site_root(context):
    root_page_class = getattr(settings, "WAGTAIL_SITE_ROOT_PAGE", 'wagtail_site.HomePage')
    root_page_model = apps.get_model(*root_page_class.split("."))
    root_page = Site.find_for_request(context["request"]).root_page
    return root_page_model.objects.get(id=root_page.id)