from django.db import models
from .conversation import Conversation
from src.apps.common.models import BaseModel
from src.apps.users.models import Users

class Message(BaseModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, related_name='message')
    sender = models.ForeignKey(Users, on_delete=models.PROTECT)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)