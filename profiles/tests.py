from unittest import TestCase, mock

from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError

from .models import User, DriverProfile, ProfileComment
from .serializers import DriverProfileCommentCreateSerializer
from .services import ProfileCommentCreateValidator, ProfileCommentValidator


class ProfileCommentValidatorTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='dasgadsfg', email='taasdfhg@gmail.com', password='123123', role='D')
        self.user = User.objects.get(username='dasgadsfg')
        self.validator = ProfileCommentValidator(self.user.id, 'driver')

    # Success case

    def test_get_driver_profile_success(self):
        self.assertEqual(DriverProfile.objects.get(user_id=self.user.id), self.validator.get_driver_profile())

    def test_get_profile_comments_success(self):
        self.assertEqual(
            [
                comment for comment in
                DriverProfile.objects.get(user_id=self.user.id).comments.exclude(parent_comment__isnull=False)
            ],
            [comment for comment in self.validator.get_profile_comments()])

    # Error case

    def test_get_driver_profile_error(self):
        self.validator.get_profile = mock.Mock(return_value=None)
        self.assertRaises(ValidationError, self.validator.get_driver_profile)

    def test_get_profile_comments_error(self):
        self.validator.get_profile = mock.Mock(return_value=None)
        self.assertRaises(ValidationError, self.validator.get_profile_comments)


class DriverProfileCommentCreateTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.get_or_create(username='dasedg123', email='12315412@gmail.com', password='123123',
                                   role='D')
        self.author_id = 1
        self.parent_id = 1

        ProfileComment.objects.create(
            content='asdgsdgsdfg',
            profile_id=1,
            comment_profile=ContentType.objects.get_for_model(DriverProfile),
            author_id=self.author_id
        )

        serializer = DriverProfileCommentCreateSerializer(data={'content': 'asdasdasd'})

        self.validator = ProfileCommentCreateValidator(
            serializer,
            1,
            self.parent_id,
            self.author_id
        )
        self.validator.get_user = mock.Mock(return_value=1)
        self.validator.get_driver_profile = mock.Mock(return_value=1)

    # Success case

    def test_get_driver_profile_id_success(self):
        self.assertEqual(1, self.validator.get_driver_profile_id())

    def test_get_author_success(self):
        self.assertEqual(User.objects.get(id=self.author_id).id, self.validator.get_author())

    def test_get_parent_comment_success(self):
        self.assertEqual(ProfileComment.objects.get(id=self.parent_id), self.validator.get_parent_comment())

    def test_update_serializer_data_success(self):
        self.assertIsNotNone(self.validator.update_serializer_data())

    # Error case

    def test_get_driver_profile_id_error(self):
        self.validator.get_driver_profile = mock.Mock(return_value=None)
        self.assertRaises(ValidationError, self.validator.get_driver_profile_id)

    def test_get_author_error(self):
        self.validator.get_user = mock.Mock(return_value=None)
        self.assertRaises(ValidationError, self.validator.get_author)

    def test_get_parent_comment_error(self):
        self.validator.get_comment = mock.Mock(return_value=None)
        self.assertRaises(ValidationError, self.validator.get_parent_comment)
