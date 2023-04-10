from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import Event
from core.entities.user import User

class IEventRepository(ABC):
    @abstractmethod
    def create(self, event: Event) -> Event:
        pass

    @abstractmethod
    def add_users_to_event(self, event: Event, users: list):
        pass

    @abstractmethod
    def update(self, id: uuid.UUID, event: Event) -> Optional[Event]:
        pass

    @abstractmethod
    def delete(self, id: uuid.UUID):
        pass

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Optional[Event]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Event]:
        pass