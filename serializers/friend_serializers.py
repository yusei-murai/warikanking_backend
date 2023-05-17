from rest_framework import serializers

class RequestFriendSerializer(serializers.Serializer):
    request_user_id=serializers.UUIDField()
    requested_user_id=serializers.UUIDField()