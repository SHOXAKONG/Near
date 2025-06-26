from rest_framework import serializers

from src.apps.users.models import Users


class BecomeEntrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'role']
        read_only_fields = ['id', 'email', 'role']
