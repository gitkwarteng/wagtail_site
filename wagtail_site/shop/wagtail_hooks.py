from wagtail import hooks
from wagtail.snippets.models import register_snippet

from wagtail_site.shop.choosers import category_chooser_view_set, classification_chooser_view_set
from wagtail_site.shop.snippets import ShopViewSetGroup

# Register viewsets
register_snippet(ShopViewSetGroup)


@hooks.register("register_admin_viewset")
def register_category_viewset():
    return category_chooser_view_set


@hooks.register("register_admin_viewset")
def register_classification_viewset():
    return classification_chooser_view_set