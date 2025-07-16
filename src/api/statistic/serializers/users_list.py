from rest_framework import serializers
from src.apps.users.models import Users


class UsersListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'role', 'is_active', 'age']
