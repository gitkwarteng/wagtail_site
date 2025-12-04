"""
In django-SHOP, a Commodity product-model is considered a very basic product without any attributes,
which can be used on a generic CMS page to describe anything.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from polymorphic.query import PolymorphicQuerySet
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin, RevisionMixin, DraftStateMixin, LockableMixin, Orderable
from wagtail.search import index

from wagtail_site.shop.models.base.fields import AutoSlugField
from wagtail_site.shop.models.base.inventory import BaseInventory
from wagtail_site.shop.models.base.product import BaseProduct, BaseProductManager, AvailableProductMixin
from wagtail_site.shop.models.base.related import BaseProductImage
from wagtail_site.shop.money.fields import MoneyField


class CommodityMixin(AvailableProductMixin):
    """
    Common methods used by both default Commodity models.
    """
    def get_price(self, request):
        return self.unit_price


class ProductQuerySet(PolymorphicQuerySet):
    pass


class ProductManager(BaseProductManager):
    queryset_class = ProductQuerySet


class Product(TranslatableMixin, DraftStateMixin, LockableMixin, RevisionMixin, CommodityMixin, BaseProduct, Orderable, ClusterableModel):
    """
    Generic Product Commodity to be used whenever the merchant does not require product specific
    attributes and just required a placeholder field to add arbitrary data.
    """
    # translatable fields for the catalog's list- and detail views
    name = models.CharField(verbose_name=_("Product name"), max_length=512)
    caption = models.CharField(verbose_name=_("Caption"), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, overwrite=True)
    code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )
    description = RichTextField("Product Details", blank=True)

    unit_price = models.DecimalField(
        _("Unit price"), max_digits=12,
        decimal_places=3,
        help_text=_("Net price for this product"),
    )

    category = models.ForeignKey(
        'shop.ProductCategory',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        help_text=_("Category"),
        related_name='commodities',
    )

    sample_image = models.ForeignKey('wagtailimages.Image',
        verbose_name=_("Sample Image"),
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        help_text=_("Sample image used in the catalog's list view."),
    )


    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock")
    )

    checkout_url = models.CharField(
        _("Checkout URL"),
        max_length=255,
        blank=True, null=True,
        help_text=_("URL to checkout page for this product if checkout is done external."),
    )


    objects = ProductManager()

    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together = ('translation_key', 'locale')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        product_page = ProductPage.objects.first()
        if product_page:
            return f'{product_page.get_url()}?product={self.slug}'
        return f'/shop/product/{self.slug}/'


class ProductImage(Orderable):

    product = ParentalKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


class ProductInventory(BaseInventory):
    """
    Inventory model for a commodity
    """
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name='inventory_set',
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Available quantity in stock")
    )

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")
        indexes = [
            models.Index(fields=['product','earliest', 'latest']),
            models.Index(fields=['product','earliest', 'latest', 'quantity']),
        ]

class ProductClassification(Orderable):
    """
    Inventory model for a commodity
    """
    product = ParentalKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name='classifications',
    )

    classification = models.ForeignKey(
        'shop.Classification',
        verbose_name=_("Classification"),
        on_delete=models.CASCADE,
        related_name='products',
    )

    class Meta:
        verbose_name = _("Product Classification")
        verbose_name_plural = _("Product Classifications")
        indexes = [
            models.Index(fields=['product','classification'])
        ]
