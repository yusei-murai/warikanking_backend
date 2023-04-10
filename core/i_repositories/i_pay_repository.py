from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import Event
from core.entities.user import User
from core.entities.pay import Pay

class IPayRepository(ABC):
    @abstractmethod
    def create(self, pay: Pay) -> Optional[Pay]:
        pass

    @abstractmethod
    def update(self, id: uuid.UUID, pay: Pay) -> Optional[Pay]:
        pass

    @abstractmethod
    def delete(self, id: uuid.UUID):
        pass

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Optional[Pay]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[list]:
        pass

    @abstractmethod
    def get_by_event_id(self, event_id: uuid.UUID) -> Optional[list]:
        pass