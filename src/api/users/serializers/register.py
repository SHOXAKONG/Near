from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from src.apps.users.models import Users


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                "password": _("Parollar mos kelmadi.")
            })

        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = Users.objects.create(
            username=validated_data['email'],
            is_active=False,
            **validated_data
        )

        user.set_password(password)
        user.save()

        return user


