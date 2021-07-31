from unittest import TestCase

from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError

from car_delivery.models import DrivingLicense
from .models import User, DriverProfile, ProfileComment
from .serializers import DriverProfileCommentCreateSerializer
from .services import ProfileCommentCreateValidator


class DriverProfileErrorsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='3qwetwetewrtw564', email='tasdf@gmail.com', password='123123', role='D')
        DrivingLicense.objects.create(title='B')

    def test_get_license_list(self):
        self.assertFalse(bool(len(DriverProfile.objects.get(id=1).license_list)))


class DriverProfileSuccessTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='dasgadsfg', email='12315412@gmail.com', password='123123',
                                   role='D')
        DrivingLicense.objects.create(title='B')

    def test_add_license(self):
        DriverProfile.objects.get(id=1).driving_license.add(1)
        self.assertTrue(bool(len(DriverProfile.objects.get(id=1).license_list)))


class DriverProfileCommentCreateSuccessTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='dasedg123', email='12315412@gmail.com', password='123123',
                                   role='D')
        self.author_id = 1
        ProfileComment.objects.create(
            content='asdgsdgsdfg',
            profile_id=1,
            comment_profile=ContentType.objects.get_for_model(DriverProfile),
            author_id=self.author_id
        )
        self.parent_id = 1
        self.validator = ProfileCommentCreateValidator(
            DriverProfileCommentCreateSerializer({'content': 'asdasdasd'}),
            1,
            self.parent_id,
            self.author_id
        )

    def test_get_driver_profile_id(self):
        self.assertEqual(1, self.validator.get_driver_profile_id())

    def test_get_author(self):
        self.assertEqual(User.objects.get(id=self.author_id), self.validator.get_author())

    def test_get_parent_comment(self):
        self.assertEqual(ProfileComment.objects.get(id=self.parent_id), self.validator.get_parent_comment())


class DriverProfileCommentCreateErrorTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='fsdfasf', email='135412@gmail.com', password='123123',
                                   role='D')
        self.author_id = 44
        self.validator = ProfileCommentCreateValidator(
            DriverProfileCommentCreateSerializer({'content': 'asdasdasd'}),
            22,
            None,
            self.author_id
        )

    def test_get_driver_profile_id(self):
        self.assertRaises(ValidationError, self.validator.get_driver_profile_id)

    def test_get_author(self):
        self.assertRaises(ValidationError, self.validator.get_author)

    def test_get_parent_comment(self):
        self.assertIsNone(self.validator.get_parent_comment())
