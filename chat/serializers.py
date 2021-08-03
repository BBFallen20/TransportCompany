from rest_framework import serializers

from profiles.serializers import UserSerializer
from .models import ChatRoom, ChatMember, ChatMessage


class ChatMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ChatMember
        fields = ['user']


class ChatMessageSerializer(serializers.ModelSerializer):
    author = ChatMemberSerializer(source='member')

    class Meta:
        model = ChatMessage
        fields = ['author', 'text', 'sent_at']


class ChatMessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['text']


class ChatRoomSerializer(serializers.ModelSerializer):
    members = ChatMemberSerializer(source='members_list', many=True)

    class Meta:
        model = ChatRoom
        fields = ['title', 'members']
