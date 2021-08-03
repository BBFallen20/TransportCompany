from django.urls import path

from .views import UserChatRoomListView, UserChatRoomMessagesListView, UserChatRoomMessageCreateView

urlpatterns = [
    path('rooms/', UserChatRoomListView.as_view(), name='user-rooms'),
    path('messages/<str:room>/', UserChatRoomMessagesListView.as_view(), name='messages-room'),
    path('messages/<str:room>/create/', UserChatRoomMessageCreateView.as_view(), name='messages-create')
]
