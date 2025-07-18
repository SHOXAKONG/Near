from rest_framework import serializers
from src.apps.history.models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'category', 'created_at', 'latitude', 'longitude']
        read_only_fields = ['id', 'user', 'created_at']
