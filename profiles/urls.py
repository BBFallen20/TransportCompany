from django.urls import path

from .views import DriverProfileUpdateView, DriverProfileCommentListView, DriverProfileCommentCreateView


urlpatterns = [
    path('driver/update/<int:pk>/', DriverProfileUpdateView.as_view(), name='driver-profile'),
    path('driver/<int:pk>/comments/', DriverProfileCommentListView.as_view(), name='driver-profile-comments'),
    path('driver/<int:pk>/comments/create/', DriverProfileCommentCreateView.as_view(), name='create-profile-comment'),
    path(
        'driver/<int:pk>/comments/<int:parent>/create/',
        DriverProfileCommentCreateView.as_view(),
        name='create-profile-comment-nested'
     ),
]
