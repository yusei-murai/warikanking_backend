from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.user import User

class IUserRepository(ABC):
    @classmethod
    @abstractmethod
    def get_by_id(cls, id: uuid.UUID) -> Optional[User]:
        pass
    
    @classmethod
    @abstractmethod
    def get_all_by_event_id(cls, event_id: uuid.UUID) -> Optional[list]:
        pass