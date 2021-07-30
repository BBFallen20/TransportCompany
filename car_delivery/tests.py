from django.test import TestCase
from rest_framework.exceptions import ValidationError

from profiles.models import User, DriverProfile
from .models import Vehicle, DrivingLicense, Race
from .services import RaceCreationValidator


class InitSetter(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='gsdfgdsf', email='danilko123@ukr.net', password='123123', role='D')
        DrivingLicense.objects.create(title='B')
        Vehicle.objects.create(model='Sonata', mark='Hyundai', drivers_limit=1, driving_category_id=1)
        Vehicle.objects.create(model='Sonata', mark='Hyundai', drivers_limit=1, driving_category_id=1)
        Race.objects.create(vehicle_id=1, driver_id=1, pickup_location='UA', supply_location='UA',
                            pickup_time='2021-09-09 10:00:00',
                            supply_time='2021-09-10 10:00:00')


class VehicleTestCase(InitSetter):
    def test_vehicle_get_drivers_count(self):
        vehicle = Vehicle.objects.get(id=1)
        self.assertEqual(vehicle.get_drivers_count, 1)
        self.assertEqual(vehicle.race_set.count(), 1)


class RaceValidatorErrorsTestCase(TestCase):
    def setUp(self) -> None:
        InitSetter().setUp()
        self.validator = RaceCreationValidator(
            {
                'vehicle': Vehicle.objects.get(id=1),
                'driver': DriverProfile.objects.get(id=1),
                'pickup_time': '2021-09-09 10:00:00',
                'supply_time': '2021-09-09 20:00:00',
            }
        )

    def test_check_limit_availability(self):
        self.assertRaises(ValidationError, self.validator.check_limit_availability)

    def test_check_driver_busy(self):
        self.assertRaises(ValidationError, self.validator.check_driver_busy)

    def test_check_driving_category(self):
        self.assertRaises(ValidationError, self.validator.check_driving_category)

    def test_complex_check(self):
        self.assertRaises(ValidationError, self.validator.check_all)


class RaceValidatorSuccessTestCase(TestCase):
    def setUp(self) -> None:
        InitSetter().setUp()
        user = User.objects.create(username='asdads', email='1234@ukr.net', password='123123', role='D')
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

    def test_check_limit_availability(self):
        self.assertIsNone(self.validator.check_limit_availability())

    def test_check_driver_busy(self):
        self.assertIsNone(self.validator.check_driver_busy())

    def test_check_driving_category(self):
        self.assertIsNone(self.validator.check_driving_category())

    def test_complex_check(self):
        self.assertIsNone(self.validator.check_all())
