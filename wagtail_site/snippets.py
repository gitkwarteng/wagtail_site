from django.urls import path
from wagtail.contrib.forms.models import FormSubmission
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.viewsets.base import ViewSet


from .models import FooterText, WebPageBanner, FormField, PageForm, TeamMember, Review
from .views import WebPageFormListView


class FooterTextViewSet(SnippetViewSet):
    model = FooterText
    icon = 'media'

    add_to_admin_menu = False
    list_display = ['body']

    # panels = ["body"]


class WebPageBannerViewSet(SnippetViewSet):
    model = WebPageBanner
    icon = 'image'
    menu_label = 'Banners'

    menu_order = 1

    add_to_admin_menu = True
    inspect_view_enabled = True
    list_display = [
        'heading',
        'image',
        'size',
        'position'
    ]
    list_filter = ['name', 'heading']


class PageFormFieldViewSet(SnippetViewSet):
    model = FormField
    icon = 'keyboard'
    menu_label = 'Fields'
    inspect_view_enabled = True
    list_display = ['label', 'field_type', 'required']


class PageFormViewSet(SnippetViewSet):
    model = PageForm
    icon = 'form'
    menu_label = 'Forms'
    inspect_view_enabled = True
    list_display = ['name', 'from_address', 'to_address']
    list_filter = ['name']


class FormSubmissionViewSet(ViewSet):
    model = FormSubmission
    icon = 'table'
    menu_label = 'Submissions'
    name = "submission"

    def get_urlpatterns(self):
        return [
            path('', WebPageFormListView.as_view(), name='index')
        ]


class FormViewSetGroup(SnippetViewSetGroup):
    items = [PageFormFieldViewSet, PageFormViewSet, FormSubmissionViewSet]
    menu_icon = 'form'
    menu_label = 'Forms'

    menu_order = 400

    add_to_admin_menu = True



class TeamMemberViewSet(SnippetViewSet):
    model = TeamMember
    icon = 'group'
    menu_label = 'Team'

    menu_order = 400

    add_to_admin_menu = True
    inspect_view_enabled = True
    list_display = [
        'name',
        'image',
        'profile',
    ]
    list_filter = ['name']


class ReviewViewSet(SnippetViewSet):
    model = Review
    icon = 'comment'
    menu_label = 'Reviews'

    menu_order = 400

    add_to_admin_menu = True
    inspect_view_enabled = True
    list_display = [
        'name',
        'image',
        'content',
    ]
    list_filter = ['name']

