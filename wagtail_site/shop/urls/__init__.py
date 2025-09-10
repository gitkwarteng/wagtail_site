from django.urls import include, path
# from wagtail_site.shop.urls import auth
from wagtail_site.shop.urls import payment


app_name = 'shop'

urlpatterns = [
    # path(r'^auth/', include(auth)),
    path(r'^payment/', include(payment)),
]
