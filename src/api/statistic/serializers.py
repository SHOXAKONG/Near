from rest_framework import serializers


class ActiveUserStatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='id')
    first_name = serializers.CharField()
    total_searches = serializers.IntegerField()

    class Meta:
        fields = ['user_id', 'first_name', 'total_searches']


class CategorySearchStatSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(source='category')
    category_name = serializers.CharField(source='category__name')
    search_count = serializers.IntegerField()

    class Meta:
        fields = ['category_id', 'category_name', 'search_count']

class DailySearchStatSerializer(serializers.Serializer):
    date = serializers.DateField()
    search_count = serializers.IntegerField()

class MonthlyStatSerializer(serializers.Serializer):
    month = serializers.DateField()
    user_registrations = serializers.IntegerField()
    category_searches = serializers.IntegerField()