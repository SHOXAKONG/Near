from rest_framework import serializers


class MonthlyStatSerializer(serializers.Serializer):
    month = serializers.DateField()
    user_registrations = serializers.IntegerField()
    category_searches = serializers.IntegerField()
