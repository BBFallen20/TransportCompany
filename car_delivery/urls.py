from django.urls import path
from .views import VehicleListView, VehicleUnusedListView, DriverListView, VehicleDriverListView, \
    RaceCreateView

urlpatterns = [
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('vehicles/unused/', VehicleUnusedListView.as_view(), name='vehicle-list-unused'),
    path('vehicles/used/', VehicleDriverListView.as_view(), name='vehicle-list-used'),
    path('race/create/', RaceCreateView.as_view(), name='vehicle-driver-create')
]
