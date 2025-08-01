

Create contact page from `AbstractFormWebPage`
```python

class ContactPage(AbstractFormWebPage, Page):
    pass

```

Use `{% include 'wagtail_site/layout/includes/site-logo.html' with logo_class="logo-dark" %}` to add site logo

Use `{% include 'wagtail_site/layout/includes/site-root.html' with root_class='tmp-btn btn-primary' %}` to add link to site root

Add these options to your settings file to customize template

```python
# wagtail.py
from pathlib import Path
from wagtail_site.settings import WagtailSiteSettings

from django_settings.settings import DatabaseConfig, DjangoDatabases


PROJECT_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = PROJECT_DIR.parent

# Database

class DatabasesSettings(DjangoDatabases):
    default = DatabaseConfig(
        engine='django.db.backends.sqlite3',
        name= BASE_DIR / "db.sqlite3"
    )


# Wagtail settings

site_settings = WagtailSiteSettings(
    wagtail_site_name="my_site",
    wagtailadmin_base_url="https://my_site.com",
    wagtail_site_style_template = 'web/layout/includes/css.html',
    wagtail_site_script_template = 'web/layout/includes/js.html',
    wagtail_site_header_template = 'web/layout/includes/header.html',
    wagtail_site_footer_template = 'web/layout/includes/footer.html',
    wagtail_site_page_template = 'web/page/index.html',
    wagtail_site_root_page = 'web.IndexPage',
    template_dirs = [BASE_DIR / 'templates'],
    databases=DatabasesSettings()
)

```