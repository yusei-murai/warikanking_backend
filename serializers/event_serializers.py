from rest_framework import serializers
from core.entities.event import Event

class RequestEventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    total = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.UUIDField())

class GetRequestEventSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

class EventSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    total = serializers.IntegerField()
    number_people = serializers.IntegerField()