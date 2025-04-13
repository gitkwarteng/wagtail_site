from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig



class AnalyticsConfig(AppConfig):
    name = 'wagtail_site.analytics'
    verbose_name = _('Analytics')

    def ready(self):
        from . import receivers  # noqa
