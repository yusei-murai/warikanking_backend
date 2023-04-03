from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import Event
from event.models import Event as EventModel
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
    
    def get_all(self) -> list[Event]:
        return super().get_all()
    

