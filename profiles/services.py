from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.response import Response

from profiles.models import User, DriverProfile


class DriverProfileUpdateValidator:
    def __init__(self, current_user: User, user_changing: User):
        self.current_user = current_user
        self.user_changing = user_changing

    def check_user_update_self_profile(self):
        if not self.current_user == self.user_changing:
            raise serializers.ValidationError({"detail": _("You can change only your profile.")})


def is_driver(func):
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
