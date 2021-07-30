from django.db import transaction
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from car_delivery.models import DrivingLicense
from .models import User, DriverProfile, ProfileComment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateDriverProfileSerializer(serializers.ModelSerializer):
    driving_license = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False, queryset=DrivingLicense.objects.all(),
    )

    class Meta:
        model = DriverProfile
        fields = ('first_name', 'last_name', 'driving_license')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.driving_license.set(validated_data['driving_license'])
        instance.save()
        return instance


class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=User.RoleChoice.choices)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.role = self.data.get('role')
        user.save()
        return user


class DriverProfileCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = ProfileComment
        fields = ['id', 'author', 'content', 'parent_comment']

    def to_representation(self, instance):
        self.fields['parent'] = DriverProfileCommentSerializer(read_only=True)
        return super(DriverProfileCommentSerializer, self).to_representation(instance)
