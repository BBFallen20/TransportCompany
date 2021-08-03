from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import ChatRoom
from chat.permissions import IsChatMember
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer


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
