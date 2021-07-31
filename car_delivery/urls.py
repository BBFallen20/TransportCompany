from django.urls import path

from .views import VehicleListView, VehicleUnusedListView, DriverListView, AllRaceListView, \
    RaceCreateView, DriverRaceListView


urlpatterns = [
    # Vehicles routing
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/unused/', VehicleUnusedListView.as_view(), name='vehicle-list-unused'),
    path('vehicles/used/', AllRaceListView.as_view(), name='vehicle-list-used'),
    # Drivers routing
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/races/<str:status>/', DriverRaceListView.as_view(), name='driver-race-list-current'),
    path('drivers/races/', DriverRaceListView.as_view(), name='driver-race-list-current'),
    # Races routing
    path('race/create/', RaceCreateView.as_view(), name='vehicle-driver-create')
]
