from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Orderable

from wagtail_site.shop import deferred
from wagtail_site.shop.models.base.product import BaseProduct


class BaseProductImage(Orderable, metaclass=deferred.ForeignKeyBuilder):
    """
    ManyToMany relation from the polymorphic Product to a set of images.
    """
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE)

    product = deferred.ForeignKey(
        BaseProduct,
        on_delete=models.CASCADE,
        related_name='images'
    )

    class Meta:
        abstract = True
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['sort_order']

ProductImageModel = deferred.MaterializedModel(BaseProductImage)
