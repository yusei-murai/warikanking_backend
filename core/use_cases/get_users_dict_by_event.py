from core.entities.event import EventId
from core.services.user_service import UserService
from core.i_repositories.i_user_repository import IUserRepository

class GetUsersDictByEventId:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    #EventIdからユーザ一覧を{UserId:Username}の形でマッピングしたものを返す
    #後々Redisを使う
    def get_users_dict_by_event_id(self, event_id: EventId):
        user_service = UserService(self.user_repo)
        event_users_list = self.user_repo.get_all_by_event_id(event_id)
        if event_users_list is None:
            return None
        
        result = user_service.mapping_user_id_name(event_users_list)

        return result