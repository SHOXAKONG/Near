from rest_framework import serializers
from src.apps.users.models import Users


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        if not Users.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is not registered')
        return value
