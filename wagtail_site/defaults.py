# from .base import INSTALLED_APPS, MIDDLEWARE, TEMPLATES

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
    "wagtail",
    "modelcluster",
    "taggit",

    'widget_tweaks'
]

WAGTAIL_MIDDLEWARE = [
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

WAGTAIL_TEMPLATES = [
    "wagtail.contrib.settings.context_processors.settings"
]


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


def add_wagtail_settings(installed_apps, middlewares, templates):

    all_required_apps = WAGTAIL_APPS

    # Update INSTALLED_APPS if your app is in it
    # updated_apps = list(settings.INSTALLED_APPS)
    for app in all_required_apps:
        if app not in installed_apps:
            installed_apps.append(app)

    # settings.INSTALLED_APPS = tuple(updated_apps)

    # add middleware
    # updated_middleware = list(settings.MIDDLEWARE)
    for mw in WAGTAIL_MIDDLEWARE:
        if mw not in middlewares:
            middlewares.append(mw)
    # settings.MIDDLEWARE = tuple(updated_middleware)

    # add templates
    # updated_templates = list(settings.TEMPLATES)
    if not templates:
        templates = [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ] + WAGTAIL_TEMPLATES,
                },
            },
        ]
    else:
        templates[0]["OPTIONS"]["context_processors"] += WAGTAIL_TEMPLATES
        for template in WAGTAIL_TEMPLATES:
            if template not in templates[0]["OPTIONS"]["context_processors"]:
                templates[0]["OPTIONS"]["context_processors"].append(template)

    # settings.TEMPLATES = tuple(updated_templates)