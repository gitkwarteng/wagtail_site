from django.conf import settings
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

app_name = 'wagtail_site'

urlpatterns = [
    path("website/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# i18urlpatterns = urlpatterns + i18n_patterns(
#     path("", include(wagtail_urls)),
#     prefix_default_language=False
# )

def get_url_patterns(localized=True):
    return urlpatterns + i18n_patterns(
        path("", include(wagtail_urls)),
        prefix_default_language=False
    ) if localized else urlpatterns
