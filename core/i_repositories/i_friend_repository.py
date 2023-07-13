from abc import ABC, abstractmethod
from typing import Optional

from core.entities.friend import Friend, FriendId, Approval
from core.entities.user import UserId

class IFriendRepository(ABC):
    @abstractmethod
    def create(self, friend: Friend) -> Optional[Friend]:
        pass

    @abstractmethod
    def update(self, id: FriendId, approval: Approval) -> Optional[Friend]:
        pass

    @abstractmethod
    def delete(self, id: FriendId):
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> Optional[list]:
        pass