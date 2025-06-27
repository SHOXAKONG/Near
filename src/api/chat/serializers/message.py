from rest_framework import serializers
from src.api.users.serializers import UserSerializer
from src.apps.chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']