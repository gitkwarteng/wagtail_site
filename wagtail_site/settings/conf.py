
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

