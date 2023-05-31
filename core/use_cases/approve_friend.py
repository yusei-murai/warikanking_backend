from core.entities.event import Event, EventName
from core.entities.user import User
from core.entities.friend import Friend, Approval, FriendId
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_friend_repository import IFriendRepository
import uuid


class ApproveFriend:
    def __init__(self, friend_repo: IFriendRepository):
        self.friend_repo = friend_repo

    def approve_friend(self, id: FriendId):
        try:
            approval = Approval(True)
            result = self.friend_repo.update(id=id, approval=approval)

            return result
        except ValueError as e:
            return str(e)
