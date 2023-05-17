import uuid
import dataclasses
from data_model.models import Friend as FriendModel
from core.entities.user import UserId

@dataclasses.dataclass(frozen=True)
class FriendId:
    id: uuid.UUID
    
@dataclasses.dataclass(frozen=True)
class FriendCreatedAt:
    created_at: str
    
@dataclasses.dataclass(frozen=True)
class Approval:
    approval: bool
    
    APPROVAL = True
    DISAPPROVAL = False

    def __post_init__(self):
        if not(self.approval == self.APPROVAL or self.approval == self.DISAPPROVAL):
            raise ValueError("only true or false")


class Friend:
    def __init__(self, id: FriendId, user_1_id: UserId, user_2_id: UserId, approval:Approval, created_at: FriendCreatedAt):
        self.id = id
        self.user_1_id = user_1_id
        self.user_2_id = user_2_id
        self.approval = approval
        self.created_at = created_at

    @classmethod
    def from_django_model(cls, friend_model: FriendModel):
        return Friend(
            id = uuid.UUID(str(friend_model.id)),
            user_1_id = friend_model.user_1_id,
            user_2_id = friend_model.user_2_id,
            approval = friend_model.approval,
            created_at = friend_model.created_at.isoformat()
        )