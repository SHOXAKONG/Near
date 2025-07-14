from rest_framework import serializers


class ActiveUserStatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='id')
    user_email = serializers.EmailField(source='email')
    total_searches = serializers.IntegerField()

    class Meta:
        fields = ['user_id', 'user_email', 'total_searches']


class CategorySearchStatSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(source='category')
    category_name = serializers.CharField(source='category__name')
    search_count = serializers.IntegerField()

    class Meta:
        fields = ['category_id', 'category_name', 'search_count']
