import uuid
from typing import Optional
import datetime

from core.entities.event import Event,EventId,IsConfirmed
from core.entities.user import UserId
from data_model.models  import Event as EventModel
from data_model.models import User as UserModel
from core.i_repositories.i_event_repository import IEventRepository

class EventRepository(IEventRepository):
    def create(self, event: Event) -> Event:
        result = EventModel.objects.create(
            id = event.id,
            name = event.name,
            is_confirmed = event.is_confirmed,
            created_at = datetime.datetime.fromisoformat(event.created_at)
        )
        
        return Event.from_django_model(result)
    
    def add_users_to_event(self, id: EventId, users: list):
        try:
            result = []
            event = EventModel.objects.get(id=id)
            for i in users:
                user = UserModel.objects.get(id=i.id)
                event.users.add(user)
                result.append(user)
                
            return result
        except EventModel.DoesNotExist:
            return None
    
    def update(self, id: EventId, event: Event) -> Optional[Event]:
        try:
            result = EventModel.objects.get(id=id)
            result.name = event.name
            result.is_confirmed = event.is_confirmed
            result.save()
            return EventModel.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
        
    def update_is_confirmed(self, id: EventId, is_confirmed: IsConfirmed) -> Optional[Event]:
        try:
            result = EventModel.objects.get(id=id)
            result.is_confirmed = is_confirmed
            result.save()
            return EventModel.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
        
    def delete(self, id: EventId):
        try:
            result = EventModel.objects.get(id=id)
            result.delete()

        except EventModel.DoesNotExist:
            pass
    
    def get_by_id(self, id: EventId) -> Optional[Event]:
        try:
            result = EventModel.objects.get(id=id)
            return Event.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
        
    def get_by_user_id(self, user_id: UserId) -> Optional[list]:
        try:
            user = UserModel.objects.prefetch_related('event_set').get(id=user_id)
            result = [Event.from_django_model(event) for event in user.event_set.order_by('-created_at')]
            return result
        
        except EventModel.DoesNotExist:
            return None