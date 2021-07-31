from django.db import transaction
from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DriverProfile, ProfileComment
from .serializers import UpdateDriverProfileSerializer, DriverProfileCommentSerializer, \
    DriverProfileCommentCreateSerializer
from .services import is_driver, DriverProfileUpdateValidator, ProfileCommentValidator, ProfileCommentCreateValidator


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
        return ProfileCommentValidator(self.kwargs.get('pk'), 'driver').get_profile_comments()


class DriverProfileCommentCreateView(CreateAPIView):
    serializer_class = DriverProfileCommentCreateSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer = ProfileCommentCreateValidator(
            serializer,
            self.kwargs.get('pk'),
            self.kwargs.get('parent')
        ).update_serializer_data()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'detail': 'Successfully created new comment.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_queryset(self):
        return ProfileComment.objects.all()
