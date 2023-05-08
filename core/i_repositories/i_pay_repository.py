from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import EventId
from core.entities.user import UserId
from core.entities.pay import Pay,PayId,RelatedUsers

class IPayRepository(ABC):
    @abstractmethod
    def create(self, pay: Pay) -> Optional[Pay]:
        pass

    @abstractmethod
    def update(self, id: PayId, pay: Pay) -> Optional[Pay]:
        pass

    @abstractmethod
    def delete(self, id: PayId):
        pass

    @abstractmethod
    def get_by_id(self, id: PayId) -> Optional[Pay]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> Optional[list]:
        pass

    @abstractmethod
    def get_by_event_id(self, event_id: EventId) -> Optional[list]:
        pass