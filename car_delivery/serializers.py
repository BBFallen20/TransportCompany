from rest_framework.serializers import ModelSerializer
from .models import Vehicle, Driver, DrivingLicense, Race
from .services import RaceCreationValidator


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


class RaceSerializer(ModelSerializer):
    vehicle = VehicleSerializer()
    driver = DriverSerializer()

    class Meta:
        model = Race
        fields = ['vehicle', 'driver']


class RaceCreateSerializer(ModelSerializer):
    def save(self, **kwargs):
        error_checker = RaceCreationValidator(self.validated_data['vehicle'], self.validated_data['driver'])
        error_checker.check_all()
        return super(RaceCreateSerializer, self).save(**kwargs)

    class Meta:
        model = Race
        fields = ['vehicle', 'driver']
