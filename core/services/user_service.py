from core.entities.event import Event,EventName
from core.entities.user import User, UserId
from core.entities.friend import Friend,Approval,FriendId
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_friend_repository import IFriendRepository
import uuid

class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
        
    def convert_user_id_name(self, id: UserId):
        result = self.user_repo.get_by_id(id)
        name = result.name
        
        return name
    
    def mapping_user_id_name(self, users: list):
        user_mapping = {user.id: user.name for user in users}
        
        return user_mapping