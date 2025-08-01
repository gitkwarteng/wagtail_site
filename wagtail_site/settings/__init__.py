from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any

from django_settings.settings import DjangoSettings

from wagtail_site.settings.conf import WAGTAIL_APPS, WAGTAIL_MIDDLEWARE, WAGTAIL_TEMPLATE_PROCESSORS


@dataclass(frozen=False, kw_only=False)
class WagtailSiteSettings(DjangoSettings):
    facebook_app_id: str = ''
    facebook_app_secret: str = ''
    instagram_app_id: str = ''
    instagram_app_secret: str = ''
    wagtailembeds_finders: List[Dict[str, str]] = field(default_factory=lambda: [])
    wagtail_content_languages: List[Tuple[str, str]] = field(default_factory=lambda: [])
    wagtail_site_style_template: str = 'wagtail_site/layout/includes/css.html'
    wagtail_site_script_template: str = 'wagtail_site/layout/includes/js.html'
    wagtail_site_header_template: str = 'wagtail_site/layout/includes/header.html'
    wagtail_site_footer_template: str = 'wagtail_site/layout/includes/footer.html'
    wagtail_site_page_template: str = 'wagtail_site/page/index.html'
    wagtail_site_root_page: str = 'web.HomePage'
    wagtail_site_name: str = 'website'
    wagtailadmin_base_url: str = 'http://localhost/admin/'
    wagtail_i18n_enabled: bool = True
    wagtaildocs_extensions: List[str] = field(default_factory=lambda: ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip'])
    wagtailsearch_backends: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        super().__post_init__()

        from wagtail.embeds.oembed_providers import youtube, vimeo, twitter, reddit, pinterest

        self.wagtailembeds_finders = [
                {
                    'class': 'wagtail.embeds.finders.facebook',
                    'app_id': self.facebook_app_id,
                    'app_secret': self.facebook_app_secret,
                },
                {
                    'class': 'wagtail.embeds.finders.instagram',
                    'app_id': self.instagram_app_id,
                    'app_secret': self.instagram_app_secret,
                },

                # Handles all other oEmbed providers the default way
                {
                    'class': 'wagtail.embeds.finders.oembed',
                    'providers': [youtube, vimeo, twitter, reddit, pinterest],
                }
            ] + self.wagtailembeds_finders

        self.wagtail_content_languages = [
            ('en', "English"),
        ] + self.wagtail_content_languages

        self.languages = [
            ('en', "English"),
        ] + self.languages or self.wagtail_content_languages

        if not self.wagtailsearch_backends:
            self.wagtailsearch_backends = {
                "default": {
                    "BACKEND": "wagtail.search.backends.database",
                }
            }

    def register(self):
        """
        Register the Django specific settings in the globals registry.
        """
        self.add_wagtail_site_settings()

        super().register()


    def add_wagtail_site_settings(self):
        # add wagtail apps
        for app in WAGTAIL_APPS:
            if app not in self.installed_apps:
                self.installed_apps.append(app)

        # add middleware
        for mw in WAGTAIL_MIDDLEWARE:
            if mw not in self.middlewares:
                self.middlewares.append(mw)

        # add template context processors
        for template in WAGTAIL_TEMPLATE_PROCESSORS:
            if template not in self.templates[0]["OPTIONS"]["context_processors"]:
                self.templates[0]["OPTIONS"]["context_processors"].append(template)
