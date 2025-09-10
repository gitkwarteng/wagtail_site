from django.db.models import PositiveIntegerField
from wagtail_site.shop.models.base import cart


class CartItem(cart.BaseCartItem):
    """Default materialized model for CartItem"""
    quantity = PositiveIntegerField()
