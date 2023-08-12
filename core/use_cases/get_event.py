from core.entities.event import Event, EventId
from core.entities.user import User,UserId
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
import uuid

class GetEvent:
    def __init__(self, event_repo: IEventRepository):
        self.event_repo = event_repo

    def get_event(self,event_id: EventId):
        result = self.event_repo.get_by_id(event_id)

        return result