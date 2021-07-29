from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response

from profiles.models import User, DriverProfile


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
