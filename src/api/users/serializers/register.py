from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from src.apps.users.models import Users


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=8, write_only=True)

    class Meta:
        model = Users
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, data):
        password = data['password']
        password_confirm = data['password_confirm']
        if password != password_confirm:
            return serializers.ValidationError('Password is do not match')
        validate_password(password)
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user


