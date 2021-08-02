from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DriverProfile, ProfileComment
from .permissions import IsOwnerUpdate, IsDriver
from .serializers import UpdateDriverProfileSerializer, DriverProfileCommentSerializer, \
    DriverProfileCommentCreateSerializer
from .services import ProfileCommentValidator, ProfileCommentCreateValidator


class DriverProfileUpdateView(UpdateAPIView):
    serializer_class = UpdateDriverProfileSerializer
    permission_classes = [IsAuthenticated, IsDriver, IsOwnerUpdate]

    def get_queryset(self):
        return DriverProfile.objects.all()


class DriverProfileCommentListView(ListAPIView):
    serializer_class = DriverProfileCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfileCommentValidator(self.kwargs.get('pk'), 'driver').get_profile_comments()


class DriverProfileCommentCreateView(CreateAPIView):
    serializer_class = DriverProfileCommentCreateSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Creating new comment to driver profile with/without parent comment"""
        serializer = self.serializer_class(data=request.data)
        serializer = ProfileCommentCreateValidator(
            serializer,
            self.kwargs.get('pk'),
            self.kwargs.get('parent'),
            self.request.user.id
        ).update_serializer_data()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'detail': _('Successfully created new comment.')},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_queryset(self):
        return ProfileComment.objects.all()
