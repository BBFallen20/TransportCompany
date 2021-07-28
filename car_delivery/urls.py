from django.urls import path
from .views import VehicleListView, VehicleUnusedListView, DriverListView, AllRaceListView, \
    RaceCreateView, DriverRaceListView

urlpatterns = [
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/races/current/', DriverRaceListView.as_view(), name='driver-race-list-current'),
    path('drivers/races/ended/', DriverRaceListView.as_view(), name='driver-race-list-ended'),
    path('drivers/races/scheduled/', DriverRaceListView.as_view(), name='driver-race-list-scheduled'),
    path('vehicles/unused/', VehicleUnusedListView.as_view(), name='vehicle-list-unused'),
    path('vehicles/used/', AllRaceListView.as_view(), name='vehicle-list-used'),
    path('race/create/', RaceCreateView.as_view(), name='vehicle-driver-create')
]
