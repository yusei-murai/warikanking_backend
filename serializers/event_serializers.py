from rest_framework import serializers
from core.entities.event import Event

class RequestEventSerializer(serializers.Serializer):
    name = serializers.CharField()
    user_ids = serializers.ListField(child=serializers.UUIDField(),required=False)
    
class AddUsersEventSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user_ids = serializers.ListField(child=serializers.CharField(),required=True)

class GetRequestEventSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

class EventSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    created_at = serializers.CharField()