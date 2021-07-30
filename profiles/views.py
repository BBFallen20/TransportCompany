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
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        DriverProfileUpdateValidator(
            current_user=request.user,
            user_changing=instance.user
        ).check_user_update_self_profile()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
