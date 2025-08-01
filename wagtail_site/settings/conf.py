
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
    # 'wagtail.locales',
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail",
    "modelcluster",
    "taggit",

    'widget_tweaks',

    "wagtail_site",
]

WAGTAIL_MIDDLEWARE = [
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    'django.middleware.locale.LocaleMiddleware'
]

WAGTAIL_TEMPLATE_PROCESSORS = [
    "wagtail.contrib.settings.context_processors.settings",
    'django.template.context_processors.i18n',
]
