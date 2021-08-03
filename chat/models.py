from django.db import models

from profiles.models import User


class ChatRoom(models.Model):
    title = models.CharField(max_length=200, verbose_name='Room title')
    members_limit = models.IntegerField(verbose_name='Chat members limit')

    def __str__(self):
        return f"Chat {self.title}"

    def __repr__(self):
        return f"Chat({self.title})"

    @property
    def members_list(self):
        return self.chatmember_set.all()

    @property
    def messages_list(self):
        return [member.chatmessage_set.all() for member in self.members_list]

    class Meta:
        verbose_name = 'Chat room'
        verbose_name_plural = 'Chat rooms'


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Chat user')
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, verbose_name='Chat')

    def __str__(self):
        return f"Chat member {self.user} - {self.chat}"

    def __repr__(self):
        return f"Chat member ({self.user} - {self.chat})"

    class Meta:
        verbose_name = 'Chat member'
        verbose_name_plural = 'Chat members'


class ChatMessage(models.Model):
    text = models.TextField(max_length=1500, verbose_name='Message text')
    member = models.ForeignKey(ChatMember, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Message to chat: {self.member.chat}"

    def __repr__(self):
        return f"Message(Chat: {self.member.chat})"

    class Meta:
        verbose_name = 'Chat message'
        verbose_name_plural = 'Chat messages'
        ordering = ['-sent_at']
