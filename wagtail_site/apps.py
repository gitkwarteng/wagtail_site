from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wagtail_site'

    def ready(self):

        print("Wagtail settings added. Be sure to add WAGTAIL_SITE_NAME and WAGTAILADMIN_BASE_URL to your settings.")
