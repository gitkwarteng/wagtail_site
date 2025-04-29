# Wagtail settings

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAIL_SITE_NAME = "portfolio"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://kwarteng.dev"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']

WAGTAIL_SITE_STYLE_TEMPLATE = 'wagtail_site/layout/includes/css.html'

WAGTAIL_SITE_SCRIPT_TEMPLATE = 'wagtail_site/layout/includes/js.html'

WAGTAIL_SITE_HEADER_TEMPLATE = 'wagtail_site/layout/includes/header.html'

WAGTAIL_SITE_FOOTER_TEMPLATE = 'wagtail_site/layout/includes/footer.html'

WAGTAIL_SITE_PAGE_TEMPLATE = 'wagtail_site/page/index.html'

WAGTAIL_SITE_ROOT_PAGE = 'wagtail_site.HomePage'