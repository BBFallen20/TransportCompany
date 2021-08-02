from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions

from profiles.models import User, DriverProfile, ProfileComment
from profiles.serializers import DriverProfileCommentCreateSerializer


class ProfileCommentValidator:
    def __init__(self, user_id: int, profile_mode: str):
        self.user_id = user_id
        self.profiles_getters = {'driver': self.get_driver_profile}
        self.profile_mode = profile_mode

    def get_profile(self):
        if DriverProfile.objects.filter(user_id=self.user_id).exists():
            return DriverProfile.objects.get(user_id=self.user_id)

    def get_driver_profile(self) -> DriverProfile:
        profile = self.get_profile()
        if profile:
            return profile
        raise exceptions.ValidationError({'detail': _('User with such id does not exist.')})

    def get_profile_comments(self) -> ProfileComment:
        profile = self.profiles_getters.get(self.profile_mode)()
        if profile:
            return profile.comments.exclude(parent_comment__isnull=False)
        raise exceptions.ValidationError({'detail': _("Profile not found.")})


class ProfileCommentCreateValidator:
    """Profile comment creating validator"""

    def __init__(self, serializer: DriverProfileCommentCreateSerializer, pk: int, parent: int or None = None,
                 author_id: int = 0):
        self.serializer = serializer
        self.pk = pk
        self.parent = parent
        self.author_id = author_id
        self.fields = {
            'author': self.get_author,
            'profile_id': self.get_driver_profile_id,
            'parent_comment': self.get_parent_comment
        }

    # Call DB methods

    def get_driver_profile(self):
        if DriverProfile.objects.filter(user_id=self.pk).exists():
            return DriverProfile.objects.get(user_id=self.pk).id

    def get_user(self) -> User or None:
        if User.objects.filter(id=self.author_id).exists():
            return User.objects.get(id=self.author_id)
        return None

    def get_comment(self):
        if ProfileComment.objects.filter(id=self.parent).exists():
            return ProfileComment.objects.get(id=self.parent)

    # Data validation

    def get_driver_profile_id(self) -> DriverProfile:
        profile = self.get_driver_profile()
        if profile:
            return profile
        raise exceptions.ValidationError({'detail': _('Profile with such id does not exist.')})

    def get_author(self) -> User:
        user = self.get_user()
        if user:
            return user
        raise exceptions.ValidationError({'detail': _('User with such id does not exist.')})

    def get_parent_comment(self) -> ProfileComment or None:
        if self.parent:
            comment = self.get_comment()
            if comment:
                return comment
            raise exceptions.ValidationError({'detail': _('Error while saving parent comment.')})
        return None

    # Return updated serializer

    def update_serializer_data(self):
        self.serializer.is_valid()
        self.serializer.validated_data['comment_profile'] = ContentType.objects.get_for_model(DriverProfile)
        for field in self.fields.keys():
            self.serializer.validated_data[field] = self.fields.get(field)()
        return self.serializer


@receiver(post_save, sender=User)
def create_user_driver_profile(sender, instance, **kwargs) -> None:
    user = instance
    if user.role == sender.RoleChoice.DRIVER:
        DriverProfile.objects.get_or_create(user=user)
