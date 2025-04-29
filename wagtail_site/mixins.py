import os
from functools import cached_property

from django.http import JsonResponse
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.forms.forms import WagtailAdminFormPageForm, FormBuilder
from wagtail.contrib.forms.models import FormSubmission
from wagtail.contrib.forms.views import SubmissionsListView

from .operations import get_form_fields_for_page
from .settings.defaults import WAGTAIL_SITE_STYLE_TEMPLATE, WAGTAIL_SITE_SCRIPT_TEMPLATE, \
    WAGTAIL_SITE_HEADER_TEMPLATE, WAGTAIL_SITE_FOOTER_TEMPLATE, WAGTAIL_SITE_PAGE_TEMPLATE
from .utils import accepts_html
from .views import FormSubmissionsListView


class PageFormMixin:
    """A mixin that adds form builder functionality to the page."""

    base_form_class = WagtailAdminFormPageForm

    form_builder = FormBuilder

    submissions_list_view_class = FormSubmissionsListView

    landing_page_template = 'wagtail_site/page/form_landing.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "landing_page_template"):
            name, ext = os.path.splitext(self.template)
            self.landing_page_template = name + "_landing" + ext

    def get_form_fields(self):
        """
        Form page expects `form` to be declared.
        """
        return get_form_fields_for_page(page=self)


    def get_data_fields(self):
        """
        Returns a list of tuples with (field_name, field_label).
        """

        data_fields = [
            ("submit_time", _("Submission date")),
        ]
        data_fields += [
            (field.clean_name, field.label) for field in self.get_form_fields()
        ]

        return data_fields

    def get_form_class(self):
        fb = self.form_builder(self.get_form_fields())
        return fb.get_form_class() if len(fb.fields) > 0 else None

    def get_form_parameters(self):
        return {}

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)

        return form_class(*args, **form_params) if form_class else None

    def get_landing_page_template(self, *args, **kwargs):
        return self.landing_page_template

    def get_submission_class(self):
        """
        Returns submission class.

        You can override this method to provide custom submission class.
        Your class must be inherited from AbstractFormSubmission.
        """

        return FormSubmission

    def get_submissions_list_view_class(self):

        return self.submissions_list_view_class or SubmissionsListView

    def process_form_submission(self, form):
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.

        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
        """

        return self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self,
        )

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        """
        Renders the landing page.

        You can override this method to return a different HttpResponse as
        landing page. E.g. you could return a redirect to a separate page.
        """
        context = self.get_context(request)
        context["form_submission"] = form_submission
        return TemplateResponse(
            request, self.get_landing_page_template(request), context
        )

    def serve_submissions_list_view(self, request, *args, **kwargs):
        """
        Returns list submissions view for admin.

        `list_submissions_view_class` can be set to provide custom view class.
        Your class must be inherited from SubmissionsListView.
        """
        results_only = kwargs.pop("results_only", False)
        view = self.get_submissions_list_view_class().as_view(results_only=results_only)
        return view(request, form_page=self, *args, **kwargs)

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = self.get_form(
                request.POST, request.FILES, page=self, user=request.user
            )

            if form and form.is_valid():
                form_submission = self.process_form_submission(form)
                return self.render_landing_page(
                    request, form_submission, *args, **kwargs
                ) if accepts_html(request) else JsonResponse({
                    "success": True,
                    "form": form.cleaned_data,
                    "message": "Submitted successfully.",
                }, status=200)
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context["form"] = form
        return TemplateResponse(request, self.get_template(request), context)

    preview_modes = [
        ("form", _("Form")),
        ("landing", _("Landing page")),
    ]

    def serve_preview(self, request, mode_name):
        if mode_name == "landing":
            return self.render_landing_page(request)
        else:
            return super().serve_preview(request, mode_name)

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["form"] = self.get_form(page=self, user=request.user)
        return context


class PageEmailForm(PageFormMixin):

    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        if self.form and self.form.to_address:
            self.form.send_mail(form)
        return submission


class DefaultTemplatesMixin:
    """A mixin that adds default templates to the page."""

    def get_context(self, request,  *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.get_templates())

        return context

    def get_templates(self):
        return {
            'style_template': self.style_template,
            'script_template':self.script_template,
            'header_template':self.header_template,
            'footer_template':self.footer_template,
            'page_template':self.page_template
        }

    @cached_property
    def style_template(self):
        return self.get_template_from_settings(
            template_name="WAGTAIL_SITE_STYLE_TEMPLATE", default=WAGTAIL_SITE_STYLE_TEMPLATE)

    @cached_property
    def script_template(self):
        return self.get_template_from_settings(
            template_name="WAGTAIL_SITE_SCRIPT_TEMPLATE", default=WAGTAIL_SITE_SCRIPT_TEMPLATE)

    @cached_property
    def header_template(self):
        return self.get_template_from_settings(
            template_name="WAGTAIL_SITE_HEADER_TEMPLATE", default=WAGTAIL_SITE_HEADER_TEMPLATE)

    @cached_property
    def footer_template(self):
        return self.get_template_from_settings(
            template_name="WAGTAIL_SITE_FOOTER_TEMPLATE", default=WAGTAIL_SITE_FOOTER_TEMPLATE)

    @cached_property
    def page_template(self):
        return self.get_template_from_settings(
            template_name="WAGTAIL_SITE_PAGE_TEMPLATE", default=WAGTAIL_SITE_PAGE_TEMPLATE)

    def get_template_from_settings(self, template_name, default):
        return getattr(settings, template_name, default)
