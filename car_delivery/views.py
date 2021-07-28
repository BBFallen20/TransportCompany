from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import Response

from .models import Vehicle, Driver, Race
from .serializers import VehicleSerializer, DriverSerializer, RaceSerializer, RaceCreateSerializer


class VehicleListView(generics.ListAPIView):
    """Vehicle objects list API"""

    def list(self, request) -> Response:
        cars = self.get_queryset()
        serializer = VehicleSerializer(cars, many=True, context={"request": request})
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

    def get_queryset(self) -> Vehicle:
        return Vehicle.objects.filter(using=False)


class DriverListView(generics.ListAPIView):
    """Driver objects list API"""
    serializer_class = DriverSerializer

    def list(self, request) -> Response:
        drivers = self.get_queryset()
        serializer = DriverSerializer(drivers, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self) -> Vehicle:
        return Driver.objects.all()


class VehicleDriverListView(generics.ListAPIView):
    """Vehicle-driver relation objects list API"""
    serializer_class = RaceSerializer

    def list(self, request) -> Response:
        vehicles_drivers = self.get_queryset()
        serializer = RaceSerializer(vehicles_drivers, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self) -> Vehicle:
        return Race.objects.all()


class VehicleDriverCreateView(generics.CreateAPIView):
    serializer_class = RaceCreateSerializer
    permission_classes = [IsAdminUser]
    queryset = Race.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
