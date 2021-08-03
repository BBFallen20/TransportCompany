from django.urls import path

from .views import UserChatRoomListView, UserChatRoomMessagesListView

urlpatterns = [
    path('rooms/', UserChatRoomListView.as_view(), name='user-rooms'),
    path('messages/<str:room>/', UserChatRoomMessagesListView.as_view(), name='messages-room')
]
