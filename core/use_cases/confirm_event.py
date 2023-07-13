from core.i_repositories.i_event_repository import IEventRepository
from core.entities.event import Event, EventId, IsConfirmed

class ConfirmEvent:
    def __init__(self, event_repo: IEventRepository):
        self.event_repo = event_repo
        
    def confirm_event(self, id: EventId):
        is_confirmed = IsConfirmed(True).is_confirmed
        return self.event_repo.update_is_confirmed(id, is_confirmed)
    