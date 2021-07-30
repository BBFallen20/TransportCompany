from django.urls import path
from .views import DriverProfileView


urlpatterns = [
    path('driver/update/<int:pk>/', DriverProfileView.as_view(), name='driver-profile')
]
