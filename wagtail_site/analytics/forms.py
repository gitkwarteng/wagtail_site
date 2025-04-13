from django import forms
from django.utils.translation import gettext_lazy as _

class PageVisitReportForm(forms.Form):
    start_date = forms.DateField(label=_("Start Date"), required=True)
    end_date = forms.DateField(label=_("End Date"), required=False)
    city = forms.CharField(label=_("City"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PageVisitAdvanceReportForm(forms.Form):
    start_date = forms.DateField(label=_("Start Date"), required=True)
    end_date = forms.DateField(label=_("End Date"), required=False)
    city = forms.CharField(label=_("City"), required=False)
    country = forms.CharField(label=_("Country"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        fields = ['start_date', 'end_date', 'city', 'country',]