from django.urls import path
from wagtail_site.shop.forms.auth import RegisterUserForm, ContinueAsGuestForm
from wagtail_site.shop.views.auth import AuthFormsView, LoginView, LogoutView, PasswordChangeView, PasswordResetRequestView

urlpatterns = [
    path(r'^password/reset/?$', PasswordResetRequestView.as_view(),
        name='password-reset-request'),
    path(r'^login/?$', LoginView.as_view(),
        name='login'),
    path(r'^register/?$', AuthFormsView.as_view(form_class=RegisterUserForm),
        name='register-user'),
    path(r'^continue/?$', AuthFormsView.as_view(form_class=ContinueAsGuestForm),
        name='continue-as-guest'),

    path(r'^logout/?$', LogoutView.as_view(),
        name='logout'),
    path(r'^password/change/?$', PasswordChangeView.as_view(),
        name='password-change'),
]
