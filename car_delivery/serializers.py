from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Vehicle, Driver, DrivingLicense, VehicleDriver
from .services import VehicleDriverCreationValidator


class DrivingLicenseSerializer(ModelSerializer):
    class Meta:
        model = DrivingLicense
        fields = ['title']


class VehicleSerializer(ModelSerializer):
    driving_category = DrivingLicenseSerializer()

    class Meta:
        model = Vehicle
        fields = ['mark', 'model', 'using', 'driving_category', 'drivers_limit']


class DriverSerializer(ModelSerializer):
    license_list = DrivingLicenseSerializer(source='get_license_list', many=True)

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'license_list']


class VehicleDriverSerializer(ModelSerializer):
    vehicle = VehicleSerializer()
    driver = DriverSerializer()

    class Meta:
        model = VehicleDriver
        fields = ['vehicle', 'driver']


class VehicleDriverCreateSerializer(ModelSerializer):
    def save(self, **kwargs):
        error_checker = VehicleDriverCreationValidator(self.validated_data['vehicle'], self.validated_data['driver'])
        error_checker.check_all()
        return super(VehicleDriverCreateSerializer, self).save(**kwargs)

    class Meta:
        model = VehicleDriver
        fields = ['vehicle', 'driver']
