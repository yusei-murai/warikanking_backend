from rest_framework import serializers
from core.entities.event import Event

class EventSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    total = serializers.IntegerField()
    number_people = serializers.IntegerField()