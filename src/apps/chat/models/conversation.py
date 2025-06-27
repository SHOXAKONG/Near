from django.db import models
from src.apps.common.models import BaseModel
from src.apps.users.models import Users


class Conversation(BaseModel):
    participants = models.ManyToManyField(Users, related_name='conversation')

    class Meta:
        db_table = 'conversation'
