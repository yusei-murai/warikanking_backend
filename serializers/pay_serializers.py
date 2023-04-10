from rest_framework import serializers
from core.entities.event import Event

class RequestPaySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    event_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    amount_pay = serializers.IntegerField()

class PaySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    event_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    amount_pay = serializers.IntegerField()