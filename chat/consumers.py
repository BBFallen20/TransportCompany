import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom
from .services.common import ChatService


class OneToOneChatConsumer(AsyncWebsocketConsumer):
    room_name: str
    room: ChatRoom
    chat_service = ChatService
    room_group_name: str
    users: list = []
    messages: dict = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chat_service = await sync_to_async(ChatService)(
            room_name=self.room_name,
            current_user=self.scope['user'],
            users=self.users,
            messages=self.messages
        )
        # If user has driver role and current members count <= max members count
        if await sync_to_async(self.chat_service.check_member_accepted, thread_sensitive=True)():
            # User will connect
            updated_data = self.chat_service.save_user()
            self.users = updated_data.get('users')
            self.messages = updated_data.get('messages')
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

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
        await sync_to_async(self.chat_service.save_message, thread_sensitive=True)(message)

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))
