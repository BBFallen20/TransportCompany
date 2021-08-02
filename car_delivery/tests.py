import datetime
from unittest import mock, TestCase

from rest_framework.exceptions import ValidationError

from profiles.models import User, DriverProfile
from .models import Vehicle, DrivingLicense, Race
from .services import RaceCreationValidator


class InitSetter(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='gsdfgdsf', email='danilko123@ukr.net', password='123123', role='D')
        DrivingLicense.objects.get_or_create(title='G')
        Vehicle.objects.create(model='Sonata', mark='Hyundai', drivers_limit=1, driving_category_id=1)
        Vehicle.objects.create(model='Sonata', mark='Hyundai', drivers_limit=1, driving_category_id=1)
        Race.objects.create(
            vehicle_id=1,
            driver_id=1,
            pickup_location='UA',
            supply_location='UA',
            pickup_time='2021-09-09 10:00:00',
            supply_time='2021-09-10 10:00:00'
        )


class RaceValidatorTestCase(TestCase):
    def setUp(self) -> None:
        InitSetter().setUp()
        User.objects.get_or_create(username='asdads', email='1234@ukr.net', password='123123', role='D')
        driver = DriverProfile.objects.get(id=2)
        driver.driving_license.add(1)
        self.validator = RaceCreationValidator(
            {
                'vehicle': Vehicle.objects.get(id=2),
                'driver': driver,
                'pickup_time': '2021-09-11 10:00:00',
                'supply_time': '2021-09-21 20:00:00',
            }
        )

    def test_check_limit_availability_success(self):
        self.assertIsNone(self.validator.check_limit_availability())

    def test_check_driver_busy_success(self):
        self.assertIsNone(self.validator.check_driver_busy())

    def test_check_driving_category_success(self):
        self.assertIsNone(self.validator.check_driving_category())

    def test_complex_check_success(self):
        self.assertIsNone(self.validator.check_all())

    def test_check_limit_availability_error(self):
        self.validator.get_vehicle_drivers_limit = mock.Mock(return_value=0)
        self.assertRaises(ValidationError, self.validator.check_limit_availability)

    def test_check_driver_busy_error(self):
        supply_time = datetime.datetime.strptime('2021-09-21 20:00:00', '%Y-%m-%d %H:%M:%S')
        pickup_time = datetime.datetime.strptime('2021-09-11 10:00:00', '%Y-%m-%d %H:%M:%S')
        race_list = [Race.objects.create(
            driver_id=1,
            vehicle_id=1,
            supply_time=supply_time,
            pickup_time=pickup_time,
            pickup_location='AS',
            supply_location='ASD'
        )]
        self.validator.get_drivers_race_list = mock.Mock(return_value=race_list)
        self.assertRaises(ValidationError, self.validator.check_driver_busy)

    def test_check_driving_category_error(self):
        self.validator.get_vehicle_driving_category = mock.Mock(return_value='C')
        self.assertRaises(ValidationError, self.validator.check_driving_category)

    def test_complex_check_error(self):
        self.validator.get_vehicle_drivers_limit = mock.Mock(return_value=0)
        self.assertRaises(ValidationError, self.validator.check_all)
