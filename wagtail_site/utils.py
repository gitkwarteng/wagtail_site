from functools import lru_cache

from django.contrib.contenttypes.models import ContentType

from wagtail import hooks
from wagtail.models import get_page_models
from wagtail.permissions import page_permission_policy


def accepts_html(request):
    accept = request.headers.get("Accept")
    return "html" in accept

def accepts_json(request):
    accept = request.headers.get("Accept")
    return "json" in accept


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def page_has_fields(page_model)->bool:
    page = page_model()
    return page.form and page.form.fields.exists()


@lru_cache(maxsize=None)
def get_form_types():
    from mixins import PageFormMixin

    form_models = [model for model in get_page_models() if issubclass(model, PageFormMixin)]

    return list(ContentType.objects.get_for_models(*form_models).values())


def get_form_pages_for_user(user):
    """
    Return a queryset of form pages that this user is allowed to access the submissions for
    """
    editable_forms = page_permission_policy.instances_user_has_permission_for(
        user, "change"
    )
    editable_forms = editable_forms.filter(content_type__in=get_form_types())

    # Apply hooks
    for fn in hooks.get_hooks("filter_form_submissions_for_user"):
        editable_forms = fn(user, editable_forms)

    return editable_forms