import uuid
from typing import Optional

from core.entities.event import Event
from core.entities.user import User
from event.models import Event as EventModel
from user.models import User as UserModel
from core.i_repositories.i_event_repository import IEventRepository

class EventRepository(IEventRepository):
    def create(self, event: Event) -> Event:
        result = EventModel.objects.create(
            id = event.id,
            name = event.name,
            total = event.total,
            number_people = event.number_people
        )
        
        return Event.from_django_model(result)
    
    def add_users_to_event(self, event: Event, users: list):
        event = EventModel.objects.get(id=event.id)
        for i in users:
            user = UserModel.objects.get(id=i.id)
            event.users.add(user)
    
    def update(self, id: uuid.UUID, event: Event) -> Optional[Event]:
        try:
            result = EventModel.objects.get(id=id)
            result.name = event.name
            result.total = event.total
            result.number_people = event.number_people
            result.save()
            return EventModel.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
    
    def delete(self, id: uuid.UUID):
        try:
            result = EventModel.objects.get(id=id)
            result.delete()

        except EventModel.DoesNotExist:
            pass
    
    def get_by_id(self, id: uuid.UUID) -> Optional[Event]:
        try:
            result = EventModel.objects.get(id=id)
            return Event.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
        
    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Event]:
        try:
            user = UserModel.objects.get(id=user_id)
            result = user.event_set.all()
            return Event.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None