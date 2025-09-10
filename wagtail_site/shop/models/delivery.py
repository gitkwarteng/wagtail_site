from django.utils.translation import gettext_lazy as _
from wagtail_site.shop.models.base.delivery import BaseDelivery


class Delivery(BaseDelivery):
    """Default materialized model for OrderShipping"""
    class Meta(BaseDelivery.Meta):
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")
