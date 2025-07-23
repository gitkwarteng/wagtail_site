

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

from wagtail_site import add_wagtail_settings

from .base import MIDDLEWARE, TEMPLATES  # Assuming you have separated settings into base.py
from .apps import INSTALLED_APPS  # and you have moved apps into apps.py

# Wagtail settings

add_wagtail_settings(INSTALLED_APPS, MIDDLEWARE, TEMPLATES)

from wagtail_site import *

WAGTAIL_SITE_NAME = "linkups"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "https://linkupsapp.com"

WAGTAIL_SITE_STYLE_TEMPLATE = 'web/layout/includes/css.html'  # path to template with your link tags

WAGTAIL_SITE_SCRIPT_TEMPLATE = 'web/layout/includes/js.html'  # path to template with your javascript  tags

WAGTAIL_SITE_HEADER_TEMPLATE = 'web/layout/includes/header.html'  # path to template with your page header

WAGTAIL_SITE_FOOTER_TEMPLATE = 'web/layout/includes/footer.html'  # path to template with your page footer

WAGTAIL_SITE_PAGE_TEMPLATE = 'web/page/index.html'  # path to template for default page

WAGTAIL_SITE_ROOT_PAGE = 'web.IndexPage'  # Your index page model

```