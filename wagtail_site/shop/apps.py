import warnings

from django.apps import AppConfig
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    name = 'wagtail_site.shop'
    verbose_name = _("Shop")
    cache_supporting_wildcard = False

    def ready(self):
        from .deferred import ForeignKeyBuilder
        # from wagtail.admin.forms.models import register_form_field_override
        # from wagtail_site.shop.money.fields import MoneyField, MoneyFieldWidget, MoneyFormField
        # from wagtail_site.shop.money import MoneyMaker
        # from wagtail_site.shop.conf import app_settings

        # perform some sanity checks
        ForeignKeyBuilder.check_for_pending_mappings()
        # currency_code = app_settings.DEFAULT_CURRENCY
        # money = MoneyMaker(currency_code)
        # widget = MoneyFieldWidget(attrs={'currency_code': money.currency})
        # defaults = {'widget': widget, 'money_class': money, 'form_class': MoneyFormField}
        #
        # register_form_field_override(MoneyField, override=defaults)

        if callable(getattr(cache, 'delete_pattern', None)):
            self.cache_supporting_wildcard = True
        else:
            warnings.warn("\n"
                "Your caching backend does not support invalidation by key pattern.\n"
                "Please use `django-redis-cache`, or wait until the product's HTML\n"
                "snippet cache expires by itself.")
        
        # Import signals for Wagtail integration
        import wagtail_site.shop.signals
