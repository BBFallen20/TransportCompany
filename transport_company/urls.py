from django.contrib import admin
from django.urls import path, include, re_path
from rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(
        r'^account-confirm-email/$',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        VerifyEmailView.as_view(),
        name='account_confirm_email'
    ),
    path('api/delivery/', include('car_delivery.urls'))
]
