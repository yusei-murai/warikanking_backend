from rest_framework import serializers

class RequestFriendSerializer(serializers.Serializer):
    user_1_id=serializers.UUIDField()
    user_2_id=serializers.UUIDField()
    