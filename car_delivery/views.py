from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import Response

from profiles.models import DriverProfile
from profiles.services import is_driver
from .models import Vehicle, Race
from .serializers import VehicleSerializer, DriverSerializer, RaceSerializer, RaceCreateSerializer


class VehicleListView(generics.ListAPIView):
    """Vehicle objects list API"""
    serializer_class = VehicleSerializer

    def list(self, request) -> Response:
        cars = self.get_queryset()
        serializer = self.serializer_class(cars, many=True, context={"request": request})
        return Response(serializer.data)

    def get_queryset(self) -> Vehicle:
        return Vehicle.objects.all()


class VehicleUnusedListView(generics.ListAPIView):
    """Unused vehicle objects list API"""
    serializer_class = VehicleSerializer

    def list(self, request) -> Response:
        cars = self.get_queryset()
        serializer = VehicleSerializer(cars, many=True, context={"request": request})
        return Response(serializer.data)

    def get_queryset(self) -> list:
        return [vehicle if vehicle.get_drivers_count == 0 else None for vehicle in Vehicle.objects.all()]


class DriverListView(generics.ListAPIView):
    """Driver objects list API"""
    serializer_class = DriverSerializer

    def list(self, request) -> Response:
        drivers = self.get_queryset()
        serializer = DriverSerializer(drivers, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self) -> Vehicle:
        return DriverProfile.objects.all()


class AllRaceListView(generics.ListAPIView):
    """Vehicle-driver relation objects list API"""
    serializer_class = RaceSerializer

    def list(self, request) -> Response:
        races = self.get_queryset()
        serializer = RaceSerializer(races, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self) -> Vehicle:
        return Race.objects.all()


class RaceCreateView(generics.CreateAPIView):
    serializer_class = RaceCreateSerializer
    permission_classes = [IsAdminUser]
    queryset = Race.objects.all()

    @transaction.atomic
    def post(self, request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class DriverRaceListView(generics.ListAPIView):
    serializer_class = RaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> Race or None:
        queries = {
            None: Race.objects.filter(driver__user=self.request.user),
            'started': Race.objects.filter(driver__user=self.request.user, status='S'),
            'pending': Race.objects.filter(driver__user=self.request.user, status='P'),
            'ended': Race.objects.filter(driver__user=self.request.user, status='E')
        }
        return queries.get(self.kwargs.get('status'))

    @is_driver
    def list(self, request, *args, **kwargs) -> Response:
        races = self.get_queryset()
        serializer = RaceSerializer(races, many=True, context={'request': request})
        return Response(serializer.data)
