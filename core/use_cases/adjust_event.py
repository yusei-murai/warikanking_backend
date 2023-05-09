from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.entities.event import EventId
from core.services.adjustment_service import AdjustmentService
        
class AdjustmentEvent:
    def __init__(self, event_repo: IEventRepository, user_repo: IUserRepository, adjustment_repo: IAdjustmentRepository):
        self.event_repo = event_repo
        self.user_repo = user_repo
        
    def adjust_event(self,event_id: EventId):
        self.adjustment_repo.delete_by_event_id(event_id)
        
        pays = self.pay_repo.get_by_event_id(event_id)
        
        AdjustmentService.adjust(event_id,pays)
        
        
        