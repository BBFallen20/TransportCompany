from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import ChatRoom, ChatMessage, ChatMember
from chat.permissions import IsChatMember
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer, ChatMessageCreateSerializer


class UserChatRoomListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.filter(chatmember__user=self.request.user)

    def list(self, request, *args, **kwargs):
        rooms = self.get_queryset()
        serializer = self.serializer_class(rooms, many=True, context={'request': request})
        return Response(serializer.data)


class UserChatRoomMessagesListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsChatMember]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room = self.kwargs.get('room')
        messages = []
        if ChatRoom.objects.filter(title=room).exists():
            for messages_list in ChatRoom.objects.get(title=room).messages_list:
                for message in messages_list:
                    messages.append(message)
        return messages

    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)


class UserChatRoomMessageCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsChatMember]
    serializer_class = ChatMessageCreateSerializer

    def get_queryset(self):
        return ChatMessage.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.validated_data['member'] = ChatMember.objects.get(
            user=self.request.user,
            chat__title=self.kwargs.get('room')
        )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'detail': _('Successfully created new message.')},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
