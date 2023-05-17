from core.entities.event import Event,EventName
from core.entities.user import User
from core.entities.friend import Friend
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_friend_repository import IFriendRepository
import uuid

class CreateFriend:
    def __init__(self, friend_repo: IFriendRepository):
        self.friend_repo = friend_repo
        
    def create_friend(self,friend: Friend):
        result = self.friend_repo.create(friend=friend)

        return result