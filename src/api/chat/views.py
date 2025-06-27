from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer, StartConversationSerializer
from src.apps.common.permissions import IsAdmin, IsParticipant
from src.apps.chat.models import Conversation, Message
from rest_framework import views
from django.utils.translation import gettext_lazy as _
from src.apps.users.models import Users

@extend_schema(tags=["Chat"])
class ConversionAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return self.request.user.conversation.all()

@extend_schema(tags=["Chat"])
class ConversationDetailAPIView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

@extend_schema(tags=["Chat"])
class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        conversation = Conversation.objects.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, conversation)
        return conversation.message.all()

@extend_schema(tags=["Chat"])
class StartConversionAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=StartConversationSerializer,
        responses={
            201: ConversationSerializer,
            200: ConversationSerializer,
        }
    )


    def post(self, request, *args, **kwargs):
        input_serializer = StartConversationSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        recipient_id = input_serializer.validated_data['recipient_id']
        recipient = get_object_or_404(Users, id=recipient_id)

        if request.user.id == recipient.id:
            return Response({"error": _("You cannot start a conversation with yourself.")},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user.role in ['user', 'entrepreneur'] and recipient.role != 'admin':
            return Response({"error": _("You can only start a conversation with an Admin.")},
                            status=status.HTTP_403_FORBIDDEN)
        if request.user.role == 'admin' and recipient.role == 'admin':
            return Response({"error": _("Admins cannot chat with other Admins in this context.")},
                            status=status.HTTP_403_FORBIDDEN)

        conversation = Conversation.objects.annotate(
            p_count=Count('participants')
        ).filter(
            participants=request.user
        ).filter(
            participants=recipient
        ).filter(
            p_count=2
        ).first()

        if conversation:
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_200_OK)

        new_conversation = Conversation.objects.create()
        new_conversation.participants.add(request.user, recipient)
        return Response(ConversationSerializer(new_conversation).data, status=status.HTTP_201_CREATED)
