from django.core.management.base import BaseCommand
from wagtail.models import Site
from wagtail_site.shop.models.pages import ShopIndexPage, ProductPage, CategoryPage
from wagtail_site.shop.models import ProductCategory


class Command(BaseCommand):
    help = 'Create Wagtail pages for existing shop products and categories'

    def handle(self, *args, **options):
        site = Site.objects.get(is_default_site=True)
        root_page = site.root_page

        # Create shop index page if it doesn't exist
        shop_index = ShopIndexPage.objects.filter(slug='shop').first()
        if not shop_index:
            shop_index = ShopIndexPage(
                title='Shop',
                slug='shop',
                description='Browse our products'
            )
            root_page.add_child(instance=shop_index)
            shop_index.save_revision().publish()
            self.stdout.write(
                self.style.SUCCESS('Created shop index page')
            )

        # Create category pages
        for category in ProductCategory.objects.all():
            if not hasattr(category, 'page'):
                category_page = CategoryPage(
                    title=category.name,
                    slug=category.slug,
                    category=category,
                    description=category.description
                )
                shop_index.add_child(instance=category_page)
                category_page.save_revision().publish()
                self.stdout.write(
                    self.style.SUCCESS(f'Created category page for {category.name}')
                )

        # Create single product page if it doesn't exist
        product_page = ProductPage.objects.filter(slug='product').first()
        if not product_page:
            product_page = ProductPage(
                title='Product',
                slug='product',
                description='Product details page'
            )
            shop_index.add_child(instance=product_page)
            product_page.save_revision().publish()
            self.stdout.write(
                self.style.SUCCESS('Created single product page')
            )