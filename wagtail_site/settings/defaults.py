# Wagtail settings
from wagtail.embeds.oembed_providers import youtube, vimeo, twitter, reddit, pinterest

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAIL_SITE_NAME = "portfolio"

WAGTAIL_I18N_ENABLED = True

LANGUAGE_CODE = 'en'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://kwarteng.dev"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']

WAGTAIL_SITE_STYLE_TEMPLATE = 'web/layout/includes/css.html'

WAGTAIL_SITE_SCRIPT_TEMPLATE = 'web/layout/includes/js.html'

WAGTAIL_SITE_HEADER_TEMPLATE = 'web/layout/includes/header.html'

WAGTAIL_SITE_FOOTER_TEMPLATE = 'web/layout/includes/footer.html'

WAGTAIL_SITE_PAGE_TEMPLATE = 'web/page/index.html'

WAGTAIL_SITE_ROOT_PAGE = 'web.HomePage'

WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'wagtail.embeds.finders.facebook',
        'app_id': 'YOUR FACEBOOK APP_ID HERE',
        'app_secret': 'YOUR FACEBOOK APP_SECRET HERE',
    },
    {
        'class': 'wagtail.embeds.finders.instagram',
        'app_id': 'YOUR INSTAGRAM APP_ID HERE',
        'app_secret': 'YOUR INSTAGRAM APP_SECRET HERE',
    },

    # Handles all other oEmbed providers the default way
    {
        'class': 'wagtail.embeds.finders.oembed',
        'providers': [youtube, vimeo, twitter, reddit, pinterest],
    }
]