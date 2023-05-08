from rest_framework import serializers
from core.entities.event import Event

class RequestPaySerializer(serializers.Serializer):
    name = serializers.CharField()
    event_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    amount_pay = serializers.IntegerField()
    related_users = serializers.ListField(child = serializers.UUIDField())
    
class GetRequestPaySerializer(serializers.Serializer):
    event_id = serializers.UUIDField()

class PaySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    event_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    amount_pay = serializers.IntegerField()