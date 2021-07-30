from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.response import Response

from profiles.models import User, DriverProfile, ProfileComment
from profiles.serializers import DriverProfileCommentCreateSerializer


class DriverProfileUpdateValidator:
    def __init__(self, current_user: User, user_changing: User):
        self.current_user = current_user
        self.user_changing = user_changing

    def check_user_update_self_profile(self):
        if not self.current_user == self.user_changing:
            raise serializers.ValidationError({"detail": _("You can change only your profile.")})


class ProfileCommentValidator:
    def __init__(self, user_id: int, profile_mode: str):
        self.user_id = user_id
        self.profiles_getters = {'driver': self.get_driver_profile}
        self.profile_mode = profile_mode

    def get_driver_profile(self) -> DriverProfile:
        if DriverProfile.objects.filter(user_id=self.user_id).exists():
            return DriverProfile.objects.filter(user__id=self.user_id).first()
        raise serializers.ValidationError({'detail': _('User with such id does not exist.')})

    def get_profile_comments(self) -> ProfileComment:
        profile = self.profiles_getters.get(self.profile_mode)()
        if profile:
            return profile.comments.exclude(parent_comment__isnull=False)
        raise serializers.ValidationError({'detail': _("Profile not found.")})


class ProfileCommentCreateValidator:
    """Profile comment creating validator"""
    def __init__(self, serializer: DriverProfileCommentCreateSerializer, pk: int, parent: int or None = None):
        self.serializer = serializer
        self.pk = pk
        self.parent = parent
        self.fields = {
            'author': self.get_author(),
            'profile_id': self.get_driver_profile_id(),
            'comment_profile': ContentType.objects.get_for_model(DriverProfile),
            'parent_comment': self.get_parent_comment() if self.parent else None
        }

    def get_driver_profile_id(self) -> DriverProfile:
        return DriverProfile.objects.get(user_id=self.get_author().id).id

    def get_author(self) -> User:
        if User.objects.filter(id=self.pk).exists():
            return User.objects.get(id=self.pk)
        raise serializers.ValidationError({'detail': _('User with such id does not exist.')})

    def get_parent_comment(self) -> ProfileComment:
        if ProfileComment.objects.filter(id=self.parent).exists():
            return ProfileComment.objects.get(id=self.parent)
        raise serializers.ValidationError({'detail': _('Error while saving parent comment.')})

    def update_serializer_data(self):
        self.serializer.is_valid()
        for field in self.fields.keys():
            self.serializer.validated_data[field] = self.fields.get(field)
        return self.serializer


def is_driver(func):
    """Decorator which check if user has role DRIVER"""
    def outer(self, request, **kwargs):
        if request.user.RoleChoice.DRIVER == request.user.role:
            return func(self, request)
        return Response({'detail': _('Driver role required to view this page.')}, 401)
    return outer


@receiver(post_save, sender=User)
def create_user_driver_profile(sender, instance, **kwargs) -> None:
    user = instance
    if user.role == sender.RoleChoice.DRIVER:
        DriverProfile.objects.get_or_create(user=user)
