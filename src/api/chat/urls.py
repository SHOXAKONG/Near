from django.urls import path
from .views import ConversionAPIView, ConversationDetailAPIView, MessageListAPIView, StartConversionAPIView

urlpatterns = [
    path('conversations/', ConversionAPIView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationDetailAPIView.as_view(), name='conversation-detail'),
    path('conversations/<int:pk>/messages/', MessageListAPIView.as_view(), name='message-list'),
    path('conversations/start/', StartConversionAPIView.as_view(), name='start-conversation'),
]