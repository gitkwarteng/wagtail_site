from django.db.models import SET_DEFAULT

from wagtail_site.shop import deferred
from wagtail_site.shop.models.base.address import BaseShippingAddress, BaseBillingAddress
from wagtail_site.shop.models.base.cart import BaseCart


class Cart(BaseCart):
    """
    Default materialized model for BaseCart containing common fields
    """
    shipping_address = deferred.ForeignKey(
        BaseShippingAddress,
        on_delete=SET_DEFAULT,
        null=True,
        default=None,
        related_name='+',
    )

    billing_address = deferred.ForeignKey(
        BaseBillingAddress,
        on_delete=SET_DEFAULT,
        null=True,
        default=None,
        related_name='+',
    )
