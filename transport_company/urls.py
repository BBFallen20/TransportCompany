from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_auth.registration.views import VerifyEmailView
from rest_framework.schemas import get_schema_view

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
    path('api/delivery/', include('car_delivery.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('openapi', get_schema_view(
                title="Transport company",
                description="API for delivery system",
                version="0.0.1"
            ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger-ui'),
]
