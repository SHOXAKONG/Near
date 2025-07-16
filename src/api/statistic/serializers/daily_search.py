from rest_framework import serializers

class DailySearchStatSerializer(serializers.Serializer):
    date = serializers.DateField()
    search_count = serializers.IntegerField()