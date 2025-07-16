from rest_framework import serializers

class CategorySearchStatSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(source='category')
    category_name = serializers.CharField(source='category__name')
    search_count = serializers.IntegerField()

    class Meta:
        fields = ['category_id', 'category_name', 'search_count']