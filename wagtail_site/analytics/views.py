from itertools import chain
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q

from apps.analytics.models import PageVisit
from apps.common.views import GeneralReportListView
from . import forms
from . import tables


class PageVisitReportListView(GeneralReportListView):
    template_name = 'analytics/grouped-analytics-report.html'
    model = PageVisit
    table_class = tables.PageVisitReportTable
    form_class = forms.PageVisitReportForm
    advance_form_class = forms.PageVisitAdvanceReportForm

    def get_table_class(self):
        return self.table_class

    def get_form_args(self):
        args = super().get_form_args()
        return args

    def get_model(self):
        return self.model

    def get_form_class(self):
        return self.form_class

    def filter_queryset(self, queryset=None):
        self.descriptions = []

        # print(form_class)
        if self.request.method == 'GET':
            self.filter_form = self.advance_form_class(self.request.GET)

        else:
            self.filter_form = self.advance_form_class()

        qs = self.queryset if queryset is None else queryset

        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data
            q_objects = Q()
            if data.get('start_date') and data.get('end_date'):
                q_objects &= Q(**{
                    f'created_at__date__gte': data['start_date'], f'created_at__date__lte': data['end_date']
                })

                self.descriptions.append(
                    _('Viewed between "{start_date}" and {end_date}').format(
                        start_date=data['start_date'].strftime("%b %d %Y"),
                        end_date=data['end_date'].strftime("%b %d %Y")
                    )
                )

            elif data.get('start_date'):
                q_objects &= Q(**{
                    f'created_at__date__gte': data['start_date']
                })
                self.descriptions.append(
                    _('Viewed on "{start_date}"').format(
                        start_date=['start_date'].strftime("%b %d %Y")
                    )
                )
            elif data.get('end_date') and len(data.get('end_date')) > 0:
                q_objects &= Q(**{
                    f'created_at__date__lte': data['end_date']
                })
                self.descriptions.append(
                    _('Date up to "{end_date}"').format(
                        end_date=['end_date'].strftime("%b %d %Y")
                    )
                )

            if data.get('city'):
                city = data['city']
                self.descriptions.append(
                    _('City is "{value}"').format(
                        value=city.title()
                    )
                )
                q_objects &= Q(**{'city__icontains': city})

            if data.get('country'):
                country = data['country']
                self.descriptions.append(
                    _('Country is "{value}"').format(
                        value=country.title()
                    )
                )
                q_objects &= Q(**{'country__icontains': country})

            qs = qs.filter(q_objects)

        else:
            today = timezone.now().strftime('%Y-%m-%d')

            self.descriptions.append(
                _('Visited Today')
            )
            qs = qs.filter(Q(**{
                f'created_at__date': today
            }))

        return qs

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-num_views')
        queryset = self.filter_queryset(queryset)
        self.queryset = queryset

        return queryset

    def get_model_group_by(self):
        return None

    def get_page_title(self):
        return _('Page Visit Report')


class GroupedPageVisitReport(PageVisitReportListView):

    def get(self, request, *args, **kwargs):
        self.group_filter = kwargs.get("group_by")
        return super().get(request, *args, **kwargs)

    def get_table_class(self):
        return self.table_class

    def get_model(self):
        return self.model

    def get_model_group_by(self):
        return self.group_filter

    def get_report_groups(self):
        if self.group_filter == 'city':
            report_groups = list(
                set(self.model.objects.values_list("city", "city")))
        elif self.group_filter == 'country':
            report_groups = list(
                set(self.model.objects.values_list("country","country")))
        elif self.group_filter == 'advert':
            report_groups = list(
                set(self.model.objects.values_list("advertiser_name","advertiser_name")))
        else:
            report_groups = list(
                set(self.model.objects.values_list("path", "path")))
        self.group_by = report_groups
        return report_groups

    def get_queryset(self):
        if self.request.GET.get('_export'):
            self.group_queryset()
            result_list = list(chain(*self.group_data))
            # print(result_list)
            # self.queryset = result_list
            return result_list
        else:
            queryset = self.group_queryset()
            return queryset if len(queryset) > 0 else self.model.objects.none()

    def group_queryset(self):
        if hasattr(self, 'group_data'):
            return self.group_data

        groups = self.get_report_groups()
        self.group_data = []
        for name, id in groups:
            if self.group_filter == 'city':
                class_qs = self.model.objects.filter(city=name)
            elif self.group_filter == 'country':
                class_qs = self.model.objects.filter(country=name)
            else:
                class_qs = self.model.objects.filter(path=name)

            filtered_qs = self.filter_queryset(class_qs)

            self.group_data.append(filtered_qs.order_by('-id'))

        return self.group_data
