from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from profiles.models import DriverProfile
from profiles.serializers import UserSerializer
from .models import Vehicle, DrivingLicense, Race
from .services import RaceCreationValidator


class DrivingLicenseSerializer(ModelSerializer):
    class Meta:
        model = DrivingLicense
        fields = ['title']


class VehicleSerializer(ModelSerializer):
    driving_category = DrivingLicenseSerializer()

    class Meta:
        model = Vehicle
        exclude = ('id',)


class DriverSerializer(ModelSerializer):
    license_list = DrivingLicenseSerializer(source='get_license_list', many=True)
    user = UserSerializer()

    class Meta:
        model = DriverProfile
        fields = ['first_name', 'last_name', 'license_list', 'rating', 'user']


class RaceSerializer(ModelSerializer):
    vehicle = VehicleSerializer()
    driver = DriverSerializer()
    status = CharField(source='get_status_display')

    class Meta:
        model = Race
        exclude = ('id',)


class RaceCreateSerializer(ModelSerializer):

    def save(self, **kwargs):
        error_checker = RaceCreationValidator(self.validated_data)
        error_checker.check_all()
        return super(RaceCreateSerializer, self).save(**kwargs)

    class Meta:
        model = Race
        exclude = ('id',)
