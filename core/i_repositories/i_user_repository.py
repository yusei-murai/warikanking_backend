from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.user import User,UserId
from core.entities.event import EventId

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: UserId) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_users_by_ids(self, id: list) -> Optional[list]:
        pass
    
    @abstractmethod
    def get_all_by_event_id(self, event_id: EventId) -> Optional[list]:
        pass