from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import Event
from core.entities.user import User

class IEventRepository(ABC):
    @classmethod
    @abstractmethod
    def create(cls, event: Event) -> Event:
        pass

    @classmethod
    @abstractmethod
    def add_users_to_event(cls, event: Event, users: list):
        pass

    @classmethod
    @abstractmethod
    def update(cls, id: uuid.UUID, event: Event) -> Optional[Event]:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, id: uuid.UUID):
        pass

    @classmethod
    @abstractmethod
    def get_by_id(cls, id: uuid.UUID) -> Optional[Event]:
        pass

    @classmethod
    @abstractmethod
    def get_by_user_id(cls, user_id: uuid.UUID) -> Optional[Event]:
        pass