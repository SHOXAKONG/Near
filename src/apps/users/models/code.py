from datetime import timedelta
from django.utils import timezone
from django.db import models
from src.apps.users.models import Users


def time_default():
    return timezone.now() + timedelta(minutes=10)

class Code(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    code = models.CharField(max_length=6, unique=True)
    expired_time = models.DateTimeField(default=time_default)

    class Meta:
        db_table = 'code'