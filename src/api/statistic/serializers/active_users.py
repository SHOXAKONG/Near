from rest_framework import serializers


class ActiveUserStatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='id')
    first_name = serializers.CharField()
    total_searches = serializers.IntegerField()

    class Meta:
        fields = ['user_id', 'first_name', 'total_searches']