from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import Event,EventId,IsConfirmed
from core.entities.user import UserId

class IEventRepository(ABC):
    @abstractmethod
    def create(self, event: Event) -> Event:
        pass

    @abstractmethod
    def add_users_to_event(self, event_id: EventId, users: list):
        pass

    @abstractmethod
    def update(self, id: EventId, event: Event) -> Optional[Event]:
        pass
    
    @abstractmethod
    def update_is_confirmed(self, id: EventId, is_confirmed: IsConfirmed) -> Optional[Event]:
        pass

    @abstractmethod
    def delete(self, id: EventId):
        pass

    @abstractmethod
    def get_by_id(self, id: EventId) -> Optional[Event]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> Optional[Event]:
        pass