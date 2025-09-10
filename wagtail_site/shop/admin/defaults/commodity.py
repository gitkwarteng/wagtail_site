from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from adminsortable2.admin import SortableAdminMixin
from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin
from wagtail_site.shop.admin.product import CMSPageAsCategoryMixin, UnitPriceMixin, CMSPageFilter
from wagtail_site.shop.models.product import Product

if settings.USE_I18N:
    from parler.admin import TranslatableAdmin


    @admin.register(Product)
    class CommodityAdmin(SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin,
                         PlaceholderAdminMixin, CMSPageAsCategoryMixin, UnitPriceMixin, admin.ModelAdmin):
        fieldsets = [
            (None, {
                'fields': [
                    ('product_name', 'slug'),
                    'caption',
                ]
            }),
            (_("Common Fields"), {
                'fields': [
                    ('product_code', 'quantity'),
                    ('unit_price', 'active'),
                    'show_breadcrumb',
                    'sample_image',
                ],
            }),
        ]
        filter_horizontal = ['cms_pages']
        list_filter = [CMSPageFilter]
        list_display = ['product_name', 'product_code', 'get_unit_price', 'active']

        def get_prepopulated_fields(self, request, obj=None):
            return {
                'slug': ['product_name'],
            }


else:

    @admin.register(Product)
    class CommodityAdmin(SortableAdminMixin, FrontendEditableAdminMixin, PlaceholderAdminMixin,
                         CMSPageAsCategoryMixin, UnitPriceMixin, admin.ModelAdmin):
        fields = [
            ('product_name', 'slug'),
            'caption',
            ('product_code', 'quantity'),
            ('unit_price', 'active'),
            'show_breadcrumb',
            'sample_image',
        ]
        filter_horizontal = ['cms_pages']
        list_filter = [CMSPageFilter]
        list_display = ['product_name', 'product_code', 'get_unit_price', 'active']
        prepopulated_fields = {'slug': ['product_name']}
