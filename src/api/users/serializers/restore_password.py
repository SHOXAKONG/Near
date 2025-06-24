from django.contrib.auth.password_validation import validate_password
from src.apps.users.models import Users
from rest_framework import serializers


class RestorePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)


    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        validate_password(password)
        return data

    def save(self, **kwargs):
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError("User not found.")
        user.set_password(self.validated_data["password"])
        user.save()
        return user
