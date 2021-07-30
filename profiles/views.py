from django.db import transaction
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DriverProfile
from .serializers import UpdateDriverProfileSerializer
from .services import is_driver, DriverProfileUpdateValidator


class DriverProfileView(UpdateAPIView):
    serializer_class = UpdateDriverProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DriverProfile.objects.all()

    @is_driver
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        DriverProfileUpdateValidator(
            current_user=request.user,
            user_changing=self.get_object().user
        ).check_user_update_self_profile()
        return self.update(request, *args, **kwargs)
