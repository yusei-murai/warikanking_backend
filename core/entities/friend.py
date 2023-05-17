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
    def __init__(self, id: FriendId, request_user_id: UserId, requested_user_id: UserId, approval: Approval, created_at: FriendCreatedAt):
        self.id = id
        self.request_user_id = request_user_id
        self.requested_user_id = requested_user_id
        self.approval = approval
        self.created_at = created_at

    @classmethod
    def from_django_model(cls, friend_model: FriendModel):
        return Friend(
            id = uuid.UUID(str(friend_model.id)),
            request_user_id = friend_model.request_user_id,
            requested_user_id = friend_model.requested_user_id,
            approval = friend_model.approval,
            created_at = friend_model.created_at.isoformat()
        )