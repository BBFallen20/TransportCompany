from rest_framework import permissions


class IsOwnerUpdate(permissions.BasePermission):
    message = 'You can change only your profile.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsDriver(permissions.BasePermission):
    message = 'Driver role required to view this page.'

    def has_permission(self, request, view):
        return request.user.RoleChoice.DRIVER == request.user.role
