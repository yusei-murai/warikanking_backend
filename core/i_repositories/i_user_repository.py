from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_by_event_id(self, event_id: uuid.UUID) -> Optional[list]:
        pass