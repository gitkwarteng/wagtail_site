from django.db import models
from django.shortcuts import get_object_or_404
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from wagtail_site.models import AbstractWebPage
from wagtail_site.shop.models.product import Product
from wagtail_site.shop.models.category import ProductCategory


class AbstractCategoryPage(AbstractWebPage):
    """Wagtail page for product categories"""

    category = models.OneToOneField(
        ProductCategory, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='page'
    )

    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        'category',
        'description',
        'banners',
    ]

    # parent_page_types = ['ShopPage']

    @route(r"^product/(?P<slug>[-\w]+)/$")  # matches /product-details/<slug>/
    def product_detail(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return self.render(request, context_overrides={"product": product, 'title': 'Product details' }, template='shop/product-detail.html')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['category'] = self.category
        context['categories'] = ProductCategory.objects.all()
        context['title'] = self.category.name
        # Get products in this category
        context['products'] = Product.objects.filter(
            category=self.category,
            active=True, live=True
        )
        return context

    class Meta:
        abstract = True
        verbose_name = "Category Page"
        verbose_name_plural = "Category Pages"


class AbstractShopPage(AbstractWebPage):
    """Main shop page listing all products"""
    
    description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        'description',
        'banners',
        'body'
    ]

    # child_page_types = ['CategoryPage']

    @route(r"^product/(?P<slug>[-\w]+)/$")  # matches /product-details/<slug>/
    def product_detail(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return self.render(request, context_overrides={"product": product, 'title': 'Product details'}, template='shop/product-detail.html')


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['products'] = Product.objects.filter(active=True, live=True)
        context['categories'] = ProductCategory.objects.all()
        return context
    
    class Meta:
        abstract = True
        verbose_name = "Shop Page"
        verbose_name_plural = "Shop Pages"