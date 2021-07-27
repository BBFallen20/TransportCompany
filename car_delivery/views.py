from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import Response

from .models import Vehicle, Driver, VehicleDriver
from .serializers import VehicleSerializer, DriverSerializer, VehicleDriverSerializer, VehicleDriverCreateSerializer


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
    serializer_class = VehicleDriverSerializer

    def list(self, request) -> Response:
        vehicles_drivers = self.get_queryset()
        serializer = VehicleDriverSerializer(vehicles_drivers, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self) -> Vehicle:
        return VehicleDriver.objects.all()


class VehicleDriverCreateView(generics.CreateAPIView):
    queryset = Vehicle.objects.filter(using=False)
    serializer_class = VehicleDriverCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
