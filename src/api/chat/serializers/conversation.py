from typing import Optional, Dict

from .message import MessageSerializer
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from src.api.users.serializers import UserSerializer
from src.apps.chat.models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'last_message']

    def get_last_message(self, obj) -> Optional[Dict]:
        last_message = obj.message.order_by('-timestamp').first()
        if not last_message:
            return None
        return MessageSerializer(last_message).data


class StartConversationSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField(help_text="The ID of the user to start a conversation with.")
