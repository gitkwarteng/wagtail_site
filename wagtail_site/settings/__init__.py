from dataclasses import dataclass, field
from functools import cached_property
from typing import List, Optional, Tuple, Dict


@dataclass(kw_only=False, frozen=False)
class WagtailSiteSettings:
    facebook_app_id: str = ''
    facebook_app_secret: str = ''
    instagram_app_id: str = ''
    instagram_app_secret: str = ''
    embed_finders: List[Dict[str, str]] = field(default_factory=lambda: [])
    content_languages: List[Tuple[str, str]] = field(default_factory=lambda: [])
    style_template: str = 'web/layout/includes/css.html'
    script_template: str = 'web/layout/includes/js.html'
    header_template: str = 'web/layout/includes/header.html'
    footer_template: str = 'web/layout/includes/footer.html'
    page_template: str = 'web/page/index.html'
    root_page: str = 'web.HomePage'
    site_name: str = 'website'
    admin_base_url: str = 'http://localhost/admin/'
    enable_localisation: bool = True
    language_code: str = 'en'
    doc_extensions: List[str] = field(default_factory=lambda: ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip'])

    @cached_property
    def as_dict(self):
        from wagtail.embeds.oembed_providers import youtube, vimeo, twitter, reddit, pinterest
        return {
            'WAGTAIL_SITE_NAME': self.site_name,
            'WAGTAIL_I18N_ENABLED': self.enable_localisation,
            'LANGUAGE_CODE': self.language_code,
            'WAGTAILADMIN_BASE_URL': self.admin_base_url,
            'WAGTAILDOCS_EXTENSIONS':self.doc_extensions,
            'WAGTAIL_SITE_STYLE_TEMPLATE': self.style_template,
            'WAGTAIL_SITE_SCRIPT_TEMPLATE': self.script_template,
            'WAGTAIL_SITE_HEADER_TEMPLATE': self.header_template,
            'WAGTAIL_SITE_FOOTER_TEMPLATE': self.footer_template,
            'WAGTAIL_SITE_PAGE_TEMPLATE': self.page_template,
            'WAGTAIL_SITE_ROOT_PAGE': self.root_page,
            'WAGTAILEMBEDS_FINDERS': [
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
            ] + self.embed_finders,
            'WAGTAIL_CONTENT_LANGUAGES': [
                ('en', "English"),
            ] + self.content_languages,
            'LANGUAGES': [
                ('en', "English"),
            ] + self.content_languages,
        }
