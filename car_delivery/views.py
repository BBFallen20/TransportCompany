from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import Response

from profiles.services import is_driver
from .models import Vehicle, Driver, Race
from .serializers import VehicleSerializer, DriverSerializer, RaceSerializer, RaceCreateSerializer
from .services import update_vehicle_status


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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        creating = super(RaceCreateView, self).create(request, *args, **kwargs)
        if creating.status_code == 201:
            transaction.savepoint_commit(sid)
            update_vehicle_status(request.POST.get('vehicle')[0])
            return creating
        else:
            transaction.savepoint_rollback(sid)
            return Response({'detail': 'Error while creating a race.'}, 400)


class DriverRaceListView(generics.ListAPIView):
    serializer_class = RaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queries = {
            'started': Race.objects.filter(driver__user=self.request.user, status='S'),
            'pending': Race.objects.filter(status='P', driver__user=self.request.user),
            'ended': Race.objects.filter(status='E', driver__user=self.request.user),
            None: Race.objects.filter(driver__user=self.request.user, status='S')
        }
        return queries.get(self.kwargs.get('status'))

    @is_driver
    def list(self, request, *args, **kwargs):
        races = self.get_queryset()
        serializer = RaceSerializer(races, many=True, context={'request': request})
        return Response(serializer.data)
