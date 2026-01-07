
WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.contrib.settings",
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail",
    "modelcluster",
    "taggit",

    'widget_tweaks',

    "post_office",
    "wagtail_site",
    "wagtail_site.shop",

]

WAGTAIL_MIDDLEWARE = [
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    'wagtail_site.shop.middleware.CustomerMiddleware'
]

WAGTAIL_TEMPLATE_PROCESSORS = [
    "wagtail.contrib.settings.context_processors.settings",
    'django.template.context_processors.i18n',
    'wagtail_site.shop.context_processors.customer',
]
