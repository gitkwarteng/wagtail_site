from decimal import Decimal as D
from decimal import InvalidOperation

from babel.numbers import format_currency
from django import template
from django.conf import settings
from django.utils.translation import get_language, to_locale

register = template.Library()


@register.filter(name='currency')
def currency(value, currency=None):
    """
    Format decimal value as currency
    """
    from wagtail_site.shop.conf import app_settings
    if currency is None:
        currency = app_settings.SHOP_DEFAULT_CURRENCY

    try:
        value = D(value)
    except (TypeError, InvalidOperation):
        return ""
    # Using Babel's currency formatting

    kwargs = {
        'currency': currency,
        'locale': to_locale(get_language() or settings.LANGUAGE_CODE)
    }

    return format_currency(value, **kwargs)
