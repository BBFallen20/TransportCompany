from django.urls import path

from .views import DriverProfileUpdateView, DriverProfileCommentListView


urlpatterns = [
    path('driver/update/<int:pk>/', DriverProfileUpdateView.as_view(), name='driver-profile'),
    path('driver/<int:pk>/comments/', DriverProfileCommentListView.as_view(), name='driver-profile-comments'),
]
