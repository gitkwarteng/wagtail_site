from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy
from wagtail.admin.ui.tables import TitleColumn
from wagtail.admin.views.pages.listing import PageListingMixin
from wagtail.contrib.forms.views import FormPagesListView, SubmissionsListView, ContentTypeColumn
from wagtail.models import Page

from .utils import get_form_pages_for_user


# Create your views here.


def get_submissions_list_view(request, *args, **kwargs):
    """Call the form page's list submissions view class"""
    page_id = kwargs.get("page_id")
    form_page = get_object_or_404(Page, id=page_id).specific
    return form_page.serve_submissions_list_view(request, *args, **kwargs)


class WebPageFormListView(FormPagesListView):

    def get_base_queryset(self):
        """Return the queryset of form pages for this view"""
        pages = get_form_pages_for_user(self.request.user).select_related("content_type")
        return self.annotate_queryset(pages)

    @classproperty
    def columns(self):
        columns = [
            col for col in PageListingMixin.columns if col.name not in {"title", "type"}
        ]
        columns.insert(
            1,
            TitleColumn(
                "title",
                classname="title",
                label=gettext_lazy("Title"),
                url_name="submissions:page-submissions",
                sort_key="title",
                width="30%",
            ),
        )
        columns.insert(
            -1,
            ContentTypeColumn(
                "content_type",
                label=gettext_lazy("Origin"),
                sort_key="content_type",
                width="20%",
            ),
        )
        return columns


class FormSubmissionsListView(SubmissionsListView):

    forms_index_url_name = "submissions:index"

    def dispatch(self, request, *args, **kwargs):
        """Check permissions and set the form page"""

        self.form_page = kwargs.get("form_page")

        if not get_form_pages_for_user(request.user).filter(pk=self.form_page.id).exists():
            raise PermissionDenied

        if self.is_export:
            data_fields = self.form_page.get_data_fields()
            # Set the export fields and the headings for spreadsheet export
            self.list_export = [field for field, label in data_fields]
            self.export_headings = dict(data_fields)

        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
