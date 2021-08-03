from chat.models import ChatMember, ChatRoom, ChatMessage


class ChatService:
    def __init__(self, room_name: str, current_user, users: list, messages: dict):
        self.room_name = room_name
        self.room_object = self.get_or_create_chatroom()
        self._current_user = current_user
        self.users = users
        self.messages = messages

    def get_messages(self):
        messages = []
        for message_set in self.room_object.messages_list:
            for message in message_set:
                messages.append(message)
        return messages

    def get_or_create_chatroom(self):
        obj, d = ChatRoom.objects.get_or_create(title=self.room_name, members_limit=2)
        return obj

    def get_or_create_chat_member(self):
        obj, d = ChatMember.objects.get_or_create(user=self._current_user, chat_id=self.room_object.id)
        return obj

    def save_message(self, message):
        """Save message to DB"""
        member = self.get_or_create_chat_member()
        ChatMessage.objects.create(text=message, member=member)

    def save_user(self):
        self.users.append(self._current_user.username)
        self.messages[self._current_user.username] = []
        return {'users': self.users, 'messages': self.messages}

    @staticmethod
    def get_member_username(member):
        return member.user.username

    @staticmethod
    def check_user_role(member):
        return member.user.RoleChoice.DRIVER == member.user.role

    def check_member_accepted(self):
        member = self.get_or_create_chat_member()
        member_role_accepted = self.check_user_role(member)
        members_count = self.get_count_chat_members()
        return members_count <= self.room_object.members_limit and member not in self.users and member_role_accepted

    def get_count_chat_members(self):
        return ChatMember.objects.filter(chat=self.room_object).count()
