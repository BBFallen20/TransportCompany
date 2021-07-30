from unittest import TestCase

from car_delivery.models import DrivingLicense
from .models import User, DriverProfile


class DriverProfileErrorsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='3qwetwetewrtw564', email='tasdf@gmail.com', password='123123', role='D')
        DrivingLicense.objects.create(title='B')

    def test_get_license_list(self):
        self.assertFalse(bool(len(DriverProfile.objects.get(id=1).get_license_list)))


class DriverProfileSuccessTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='dasgadsfg', email='12315412@gmail.com', password='123123',
                                   role='D')
        DrivingLicense.objects.create(title='B')

    def test_add_license(self):
        DriverProfile.objects.get(id=1).driving_license.add(1)
        self.assertTrue(bool(len(DriverProfile.objects.get(id=1).get_license_list)))


class DriverProfileCommentTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='dasedg123', email='12315412@gmail.com', password='123123',
                                   role='D')
