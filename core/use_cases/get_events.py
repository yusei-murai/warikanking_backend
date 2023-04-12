from core.entities.event import Event
from core.entities.user import User
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
import uuid

class GetEvents:
    def __init__(self, event_repo: IEventRepository):
        self.event_repo = event_repo

    def get_events(self,user_id: uuid.UUID):
        result = self.event_repo.get_by_user_id(user_id)

        return result