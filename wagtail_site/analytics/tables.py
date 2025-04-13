import django_tables2 as tables

from apps.analytics.models import PageVisit


class PageVisitReportTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PageVisit
        fields = ['path','contry','city','ip_address']
        attrs = {"class": "table table-shadow table-striped w-100","id":"page_visti_table",'tf':{'class':'text-end'}}
