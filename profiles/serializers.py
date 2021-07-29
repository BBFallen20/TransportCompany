from rest_framework import serializers
from django.db import transaction
from rest_auth.registration.serializers import RegisterSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=User.RoleChoice.choices)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.role = self.data.get('role')
        user.save()
        return user
