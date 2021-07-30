from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DriverProfile, ProfileComment
from .serializers import UpdateDriverProfileSerializer, DriverProfileCommentSerializer
from .services import is_driver, DriverProfileUpdateValidator


class DriverProfileUpdateView(UpdateAPIView):
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


class DriverProfileCommentListView(ListAPIView):
    serializer_class = DriverProfileCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        driver_profile = DriverProfile.objects.filter(user__id=self.kwargs.get('pk')).first()
        if driver_profile:
            comments = ProfileComment.objects.filter(
                profile_id=driver_profile.id,
                comment_profile=ContentType.objects.get_for_model(driver_profile).id,
            )
            return comments
        raise serializers.ValidationError({'detail': "Profile not found."})
