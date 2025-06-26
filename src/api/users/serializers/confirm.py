from django.utils import timezone
from rest_framework import serializers
from src.apps.users.models import Code
from django.utils.translation import gettext_lazy as _

class ConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        try:
            code = Code.objects.get(code=value)
        except Code.DoesNotExist:
            raise serializers.ValidationError(_('Code is not correct'))

        if code.expired_time < timezone.now():
            raise serializers.ValidationError(_('Code has expired'))
        return value
