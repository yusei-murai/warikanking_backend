from abc import ABC, abstractmethod
import uuid
from typing import Optional

from core.entities.event import EventId
from core.entities.user import UserId
from core.entities.pay import Pay,PayId
from core.entities.adjustment import Adjustment,AdjustmentId

class IAdjustmentRepository(ABC):
    @abstractmethod
    def create(self, adjustment: Adjustment) -> Optional[Adjustment]:
        pass
    
    @abstractmethod
    def create_many(self, adjustment_list: list) -> Optional[list]:
        pass

    @abstractmethod
    def update(self, id: AdjustmentId, adjustment: Adjustment) -> Optional[Adjustment]:
        pass

    @abstractmethod
    def delete(self, id: AdjustmentId):
        pass
    
    @abstractmethod
    def delete_by_event_id(self, event_id: EventId):
        pass

    @abstractmethod
    def get_by_id(self, id: AdjustmentId) -> Optional[Adjustment]:
        pass

    @abstractmethod
    def get_by_adjust_user_id(self, user_id: UserId) -> Optional[list]:
        pass
    
    @abstractmethod
    def get_by_event_id(self, event_id: EventId):
        pass