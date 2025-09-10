from cms.models.static_placeholder import StaticPlaceholder
from django.core.management.base import BaseCommand, CommandError
from cmsplugin_cascade.models import CascadeClipboard
from shop.management.utils import deserialize_to_placeholder


class MissingPage(CommandError):
    """
    Exception class indicating that a CMS page with a predefined ``reverse_id`` is missing.
    """


class MissingAppHook(CommandError):
    """
    Exception class indicating that a page misses the application.
    """


class MissingPlugin(CommandError):
    """
    Exception class indicating that a special plugin is missing or misconfigured on a given
    CMS page.
    """


class Command(BaseCommand):
    help = "Commands for Django-SHOP."

    def add_arguments(self, parser):
        parser.add_argument(
            'subcommand',
            help="./manage.py shop [customers|check-pages|review-settings]",
        )
        parser.add_argument(
            '--delete-expired',
            action='store_true',
            dest='delete_expired',
            help="Delete customers with expired sessions.",
        )
        parser.add_argument(
            '--add-missing',
            action='store_true',
            dest='add_missing',
            default=False,
            help="Use in combination with 'check-pages' to add missing mandatory pages.",
        )
        parser.add_argument(
            '--add-recommended',
            action='store_true',
            dest='add_recommended',
            default=False,
            help="Use in combination with 'check-pages' to add missing recommended pages.",
        )

    def handle(self, verbosity, subcommand, *args, **options):
        if subcommand == 'help':
            self.stdout.write("""
Usage:

./manage.py shop customers
    Show how many customers are registered, guests, anonymous or expired.            
    Use option --delete-expired to delete all customers with an expired session.            

./manage.py shop check-pages
    Iterate over all pages in the CMS and check, if they are properly configured.
    Use option --add-missing to add all missing mandatory pages for this shop.
    Use option --add-recommended to also add missing but recommended pages for this shop.

./manage.py shop review-settings
    Review all shop related settings and complain about missing- or mis-configurations.
""")
        elif subcommand == 'customers':
            self.delete_expired = options['delete_expired']
            self.customers()
        elif subcommand == 'check-pages':
            self.stdout.write("The following CMS pages must be adjusted:")
            self.add_recommended = options['add_recommended']
            self.add_mandatory = options['add_missing'] or self.add_recommended
            self.personal_pages = self.impersonal_pages = None
            if self.add_recommended:
                for k, msg in enumerate(self.create_recommended_pages(), 1):
                    self.stdout.write(" {}. {}".format(k, msg))
            for k, msg in enumerate(self.check_mandatory_pages(), 1):
                self.stdout.write(" {}. {}".format(k, msg))
        elif subcommand == 'review-settings':
            self.stdout.write("The following configuration settings must be fixed:")
            for k, msg in enumerate(self.review_settings(), 1):
                self.stdout.write(" {}. {}".format(k, msg))
        else:
            msg = "Unknown sub-command for shop. Use one of: customer check-pages review-settings"
            self.stderr.write(msg.format(subcommand))

    def customers(self):
        """
        Entry point for subcommand ``./manage.py shop customers``.
        """
        from wagtail_site.shop.models.base.customer import CustomerModel

        data = dict(total=0, anonymous=0, active=0, staff=0, guests=0, registered=0, expired=0)
        for customer in CustomerModel.objects.iterator():
            data['total'] += 1
            if customer.user.is_active:
                data['active'] += 1
            if customer.user.is_staff:
                data['staff'] += 1
            if customer.is_registered:
                data['registered'] += 1
            elif customer.is_guest:
                data['guests'] += 1
            elif customer.is_anonymous:
                data['anonymous'] += 1
            if customer.is_expired:
                data['expired'] += 1
                if self.delete_expired and customer.orders.count() == 0:
                    customer.delete()
        msg = "Customers in this shop: total={total}, anonymous={anonymous}, expired={expired}, active={active}, guests={guests}, registered={registered}, staff={staff}."
        self.stdout.write(msg.format(**data))


    def assign_all_products_to_page(self, page):
        from wagtail_site.shop.models.base.product import ProductModel
        from wagtail_site.shop.models.base.related import ProductPageModel

        for product in ProductModel.objects.all():
            ProductPageModel.objects.create(page=page, product=product)

    def review_settings(self):
        from django.conf import settings

        if getattr(settings, 'AUTH_USER_MODEL', None) != 'email_auth.User':
            yield "settings.AUTH_USER_MODEL should be 'email_auth.User'."

        AUTHENTICATION_BACKENDS = getattr(settings, 'AUTHENTICATION_BACKENDS', [])
        if 'allauth.account.auth_backends.AuthenticationBackend' not in AUTHENTICATION_BACKENDS:
            yield "settings.AUTHENTICATION_BACKENDS should contain 'allauth.account.auth_backends.AuthenticationBackend'."

        if 'sass_processor.finders.CssFinder' not in getattr(settings, 'STATICFILES_FINDERS', []):
            yield "settings.STATICFILES_FINDERS should contain 'sass_processor.finders.CssFinder'."

        if 'node_modules' not in dict(getattr(settings, 'STATICFILES_DIRS', [])).keys():
            yield "settings.STATICFILES_DIRS should contain ('node_modules', '/…/node_modules')."

        if '/node_modules/' not in getattr(settings, 'NODE_MODULES_URL', ''):
            yield "settings.NODE_MODULES_URL should start with a URL pointing onto /…/node_modules/."

        for template_engine in getattr(settings, 'TEMPLATES', []):
            if template_engine['BACKEND'] != 'django.template.backends.django.DjangoTemplates':
                continue
            context_processors = template_engine['OPTIONS'].get('context_processors', [])
            if 'shop.context_processors.customer' not in context_processors:
                yield "'shop.context_processors.customer' is missing in 'context_processors' of the default Django Template engine."
            if 'shop.context_processors.shop_settings' not in context_processors:
                yield "'shop.context_processors.shop_settings' is missing in 'context_processors' of the default Django Template engine."
        for template_engine in getattr(settings, 'TEMPLATES', []):
            if template_engine['BACKEND'] == 'post_office.template.backends.post_office.PostOfficeTemplates':
                break
        else:
            yield "In settings.TEMPLATES, the backend for 'post_office.template.backends.post_office.PostOfficeTemplates' is missing."

        if getattr(settings, 'POST_OFFICE', {}).get('TEMPLATE_ENGINE') != 'post_office':
            yield "settings.POST_OFFICE should contain {'TEMPLATE_ENGINE': 'post_office'}."

        for dir in getattr(settings, 'SASS_PROCESSOR_INCLUDE_DIRS', []):
            if '/node_modules' in dir:
                break
        else:
            yield "settings.SASS_PROCESSOR_INCLUDE_DIRS should include the folder '…/node_modules'."

        if getattr(settings, 'COERCE_DECIMAL_TO_STRING', None) is not True:
            yield "settings.COERCE_DECIMAL_TO_STRING should be set to 'True'."

        if getattr(settings, 'FSM_ADMIN_FORCE_PERMIT', None) is not True:
            yield "settings.FSM_ADMIN_FORCE_PERMIT should be set to 'True'."

        if getattr(settings, 'SERIALIZATION_MODULES', {}).get('json') != 'shop.money.serializers':
            yield "settings.SERIALIZATION_MODULES['json'] should be set to 'shop.money.serializers'."

        REST_FRAMEWORK = getattr(settings, 'REST_FRAMEWORK', {})
        if 'shop.rest.money.JSONRenderer' not in REST_FRAMEWORK.get('DEFAULT_RENDERER_CLASSES', []):
            yield "settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] should contain class 'shop.rest.money.JSONRenderer'."

        if 'django_filters.rest_framework.DjangoFilterBackend' not in REST_FRAMEWORK.get('DEFAULT_FILTER_BACKENDS', []):
            yield "settings.REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] should contain class 'django_filters.rest_framework.DjangoFilterBackend'."

        if getattr(settings, 'REST_AUTH_SERIALIZERS', {}).get('LOGIN_SERIALIZER') != 'shop.serializers.auth.LoginSerializer':
            yield "settings.REST_AUTH_SERIALIZERS['LOGIN_SERIALIZER'] should be set to 'shop.serializers.auth.LoginSerializer'."

        if 'shop.cascade' not in getattr(settings, 'CMSPLUGIN_CASCADE_PLUGINS', []):
            yield "settings.CMSPLUGIN_CASCADE_PLUGINS should contain entry 'shop.cascade'."

        CMSPLUGIN_CASCADE = getattr(settings, 'CMSPLUGIN_CASCADE', {})
        if CMSPLUGIN_CASCADE.get('link_plugin_classes') != [
            'shop.cascade.plugin_base.CatalogLinkPluginBase',
            'cmsplugin_cascade.link.plugin_base.LinkElementMixin',
            'shop.cascade.plugin_base.CatalogLinkForm']:
            yield "settings.CMSPLUGIN_CASCADE['link_plugin_classes'] should contain special classes able to link onto products."
        if CMSPLUGIN_CASCADE.get('bootstrap4', {}).get('template_basedir') != 'angular-ui':
            yield "settings.CMSPLUGIN_CASCADE['bootstrap4']['template_basedir'] should be 'angular-ui'."
        if CMSPLUGIN_CASCADE.get('segmentation_mixins') != [
            ('shop.cascade.segmentation.EmulateCustomerModelMixin',
             'shop.cascade.segmentation.EmulateCustomerAdminMixin')]:
            yield "settings.CMSPLUGIN_CASCADE['segmentation_mixins'] should contain a special version handling the Customer model."

        if not isinstance(getattr(settings, 'SHOP_CART_MODIFIERS', None), (list, tuple)):
            yield "settings.SHOP_CART_MODIFIERS should contain a list with cart modifiers."
