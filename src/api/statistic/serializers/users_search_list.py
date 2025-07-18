from rest_framework import serializers
from src.apps.history.models import SearchHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.first_name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SearchHistory
        fields = [
            'id',
            'user',
            'category',
            'latitude',
            'longitude',
            'created_at'
        ]