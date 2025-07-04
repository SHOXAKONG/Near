from src.apps.users.models import Users
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'role']



