from core.i_repositories.i_event_repository import IEventRepository
from core.entities.event import EventId

class AddUsersEvent:
    def __init__(self, event_repo: IEventRepository):
        self.event_repo = event_repo
        
    def add_users_event(self, event_id: EventId, users: list):
        result = self.event_repo.add_users_to_event(event_id, users)
        
        return result