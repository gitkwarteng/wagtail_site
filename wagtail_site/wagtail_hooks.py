from wagtail.snippets.models import register_snippet
from wagtail import hooks

from .choosers import banner_chooser_viewset, form_field_chooser_viewset, page_form_chooser_viewset, review_chooser_viewset, team_member_chooser_viewset

from .snippets import WebPageBannerViewSet, FormViewSetGroup, ReviewViewSet, TeamMemberViewSet

register_snippet(FormViewSetGroup)
register_snippet(WebPageBannerViewSet)
register_snippet(ReviewViewSet)
register_snippet(TeamMemberViewSet)


@hooks.register("register_admin_viewset")
def register_banner_viewset():
    return banner_chooser_viewset


@hooks.register("register_admin_viewset")
def register_form_field_viewset():
    return form_field_chooser_viewset


@hooks.register("register_admin_viewset")
def register_form_viewset():
    return page_form_chooser_viewset


@hooks.register("register_admin_viewset")
def register_team_viewset():
    return team_member_chooser_viewset


@hooks.register("register_admin_viewset")
def register_review_viewset():
    return review_chooser_viewset

