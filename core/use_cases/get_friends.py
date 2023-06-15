from core.i_repositories.i_friend_repository import IFriendRepository
from core.entities.user import UserId

class GetFriends:
    def __init__(self,friend_repo: IFriendRepository):
        self.friend_repo = friend_repo
        
    def get_friend(self,user_id: UserId):
        result = self.friend_repo.get_by_user_id(user_id)
        
        return result