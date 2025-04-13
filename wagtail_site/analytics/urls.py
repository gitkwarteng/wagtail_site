from django.urls import path, include
from apps.common import views as common_views
from apps.analytics import views as analytics_views
from apps.common import permissions_required
from greyspace.settings import DASHBOARD_LOGIN_URL


app_name = "analytics"
urlpatterns = [
    # path('general/', include([
        path('advertiser/',
                 permissions_required(['analytics.view_advertiser'], DASHBOARD_LOGIN_URL)(common_views.GeneralListView.as_view()),
                 name="advertiser"),

        path('advertiser/add/',
                 permissions_required(['analytics.add_advertiser'], DASHBOARD_LOGIN_URL)(common_views.CreateUpdateView.as_view()),
                 name="add_advertiser"),

        path('advertiser/<int:pk>/edit/',
                 permissions_required(['analytics.change_advertiser'], DASHBOARD_LOGIN_URL)(common_views.CreateUpdateView.as_view()),
                 name="edit_advertiser"),

        path('advertiser/<int:pk>/delete/',
                 permissions_required(['analytics.delete_advertiser'], DASHBOARD_LOGIN_URL)(common_views.delete_object_view),
                 name="delete_advertiser"),

        path('advertiser/add_bulk/',
                 permissions_required(['analytics.add_advertiser'], DASHBOARD_LOGIN_URL)(common_views.GenericBulkCreateView.as_view()),
                 name="bulk_advertiser"),

        path('advertiser/import/',
                 permissions_required(['analytics.add_advertiser'], DASHBOARD_LOGIN_URL)(common_views.GenericImportView.as_view()),
                 name="import_advertiser"),
    # ]))
]

# # report patterns
urlpatterns += [
    path('report/', include([
        path('analytics/page-visit/<str:group_by>/',
                     permissions_required(['analytics.view_pagevisit'], DASHBOARD_LOGIN_URL)(analytics_views.GroupedPageVisitReport.as_view()),
                     name="page-visit-report"),

    ]))  #
]