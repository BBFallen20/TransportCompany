import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, ChatMember, ChatMessage


class OneToOneChatConsumer(AsyncWebsocketConsumer):
    room_name: str
    room: ChatRoom
    room_group_name: str
    users: list = []
    messages: dict = {}

    def get_count_chat_members(self):
        return ChatMember.objects.filter(chat=self.room).count()

    @staticmethod
    def check_user_role(member):
        return member.user.RoleChoice.DRIVER == member.user.role

    def get_messages(self):
        messages = []
        for message_set in self.room.messages_list:
            for message in message_set:
                messages.append(message)
        return messages

    def get_or_create_chatroom(self):
        obj, d = ChatRoom.objects.get_or_create(title=self.room_name, members_limit=2)
        return obj

    def get_or_create_chat_member(self):
        obj, d = ChatMember.objects.get_or_create(user=self.scope['user'], chat_id=self.room.id)
        return obj

    def check_member_accepted(self):
        member = self.get_or_create_chat_member()
        member_role_accepted = self.check_user_role(member)
        members_count = self.get_count_chat_members()
        return members_count <= self.room.members_limit and member not in self.users and member_role_accepted

    def save_message(self, message):
        """Save message to DB"""
        member = self.get_or_create_chat_member()
        ChatMessage.objects.create(text=message, member=member)

    def save_user(self):
        self.users.append(self.scope['user'].username)
        self.messages[self.scope['user'].username] = []

    @staticmethod
    def get_member_username(member):
        return member.user.username

    async def initialize_chat(self):
        """Sending existing chat messages"""
        for message in await sync_to_async(self.get_messages, thread_sensitive=True)():
            user = await sync_to_async(self.get_member_username, thread_sensitive=True)(message.member)
            if message.text not in self.messages[self.scope['user'].username]:
                await self.send(text_data=json.dumps({
                    'message': message.text,
                    'user': user,
                }))
                self.messages[self.scope['user'].username].append(message.text)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        room = await sync_to_async(self.get_or_create_chatroom, thread_sensitive=True)()
        self.room = room
        # If user has driver role and current members count <= max members count
        if await sync_to_async(self.check_member_accepted, thread_sensitive=True)():
            # User will connect
            self.save_user()
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            # Initialize existing chat messages and send them to the user
            await self.initialize_chat()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].username
            }
        )
        await sync_to_async(self.save_message, thread_sensitive=True)(message)

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))
