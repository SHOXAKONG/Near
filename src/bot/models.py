from django.db import models
from src.apps.users.models import Users


class TelegramProfile(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name='telegram_profile',
        null=True,
        blank=True
    )
    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    step = models.CharField(max_length=100, default='default')
    language = models.CharField(max_length=2, default='uz')
    temp_data = models.JSONField(default=dict, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    is_entrepreneur = models.BooleanField(default=False, verbose_name="Tadbirkormi?")

    def __str__(self):
        if self.user:
            return f"{self.user.username} ({self.tg_id})"
        return str(self.tg_id)

    class Meta:
        verbose_name = "Telegram Profile"
        verbose_name_plural = "Telegram Profiles"