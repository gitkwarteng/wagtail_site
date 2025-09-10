from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting

from wagtail_site.shop.money.iso4217 import CURRENCY_CHOICES


@register_setting(icon='sliders')
class ShopSettings(BaseGenericSetting):
    default_currency = models.CharField(
        verbose_name="Default currency",
        help_text="The default currency for the shop.",
        max_length=3, default="USD", choices=CURRENCY_CHOICES)
    vendor_email = models.CharField(
        verbose_name="Vendor email",
        help_text="The email address to which vendor notifications are sent.",
        max_length=255, blank=True, null=True)
    money_format = models.CharField(
        verbose_name="Money format",
        max_length=50, blank=True, null=True, default='{symbol} {amount}',
        help_text="""
        When rendering an amount of type Money, use this format.
        Possible placeholders are:
        * ``{symbol}``: This is replaced by €, $, £, etc.
        * ``{currency}``: This is replaced by Euro, US Dollar, Pound Sterling, etc.
        * ``{code}``: This is replaced by EUR, USD, GBP, etc.
        * ``{amount}``: The localized amount.
        * ``{minus}``: Only for negative amounts, where to put the ``-`` sign.
        """)
    decimal_places = models.PositiveSmallIntegerField(default=2)
    max_purchase_quantity = models.PositiveSmallIntegerField(
        verbose_name="Maximum purchase quantity",
        help_text="The maximum quantity of a product that can be purchased in a single order.",
        default=99)
    value_added_tax = models.DecimalField(
        verbose_name="Value added tax",
        help_text="The value added tax in percent.",
        max_digits=4, decimal_places=2, default=19.0)

    override_shipping_method = models.BooleanField(
        verbose_name="Override shipping method",
        help_text="If checked, the merchant can override the shipping method chosen by customer during processing.",
        default=False)


    panels = [
        'default_currency',
        'money_format',
        'decimal_places',
        'value_added_tax',
        'max_purchase_quantity',
        'vendor_email',
        'override_shipping_method',
    ]
