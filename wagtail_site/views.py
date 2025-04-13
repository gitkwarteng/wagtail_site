from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import gettext
from django.views import View
from wagtail.contrib.forms.views import FormPagesListView, SubmissionsListView

from .utils import get_form_pages_for_user


# Create your views here.

class WebPageFormListView(FormPagesListView):

    def get_base_queryset(self):
        """Return the queryset of form pages for this view"""
        pages = get_form_pages_for_user(self.request.user).select_related("content_type")
        return self.annotate_queryset(pages)


class FormSubmissionsListView(SubmissionsListView):

    forms_index_url_name = "submission:index"

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
