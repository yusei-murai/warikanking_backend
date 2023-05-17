from core.entities.event import Event,EventName
from core.entities.user import User
from core.entities.friend import Friend,Approval
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_friend_repository import IFriendRepository
import uuid

class RequestFriend:
    def __init__(self, friend_repo: IFriendRepository):
        self.friend_repo = friend_repo
        
    def request_friend(self,friend: Friend):
        friend.approval = Approval(False)
        
        result = self.friend_repo.create(friend=friend)

        return result