from rest_framework import permissions

from chat.models import ChatMember


class IsChatMember(permissions.BasePermission):
    message = 'You need to be a chat member.'

    def has_permission(self, request, view):
        if ChatMember.objects.filter(chat__title=view.kwargs.get('room'), user=request.user).exists():
            return True
        return False
