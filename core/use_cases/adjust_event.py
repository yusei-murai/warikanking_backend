from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_pay_repository import IPayRepository
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.entities.event import EventId
from core.services.adjustment_service import AdjustmentService
        
class AdjustmentEvent:
    def __init__(self, event_repo: IEventRepository, pay_repo: IPayRepository, adjustment_repo: IAdjustmentRepository):
        self.event_repo = event_repo
        self.pay_repo = pay_repo
        self.adjustment_repo = adjustment_repo
        
    def adjust_event(self,event_id: EventId):
        self.adjustment_repo.delete_by_event_id(event_id) #元々のadjustmentを全て削除
        pays = self.pay_repo.get_by_event_id(event_id)
        
        result = AdjustmentService.adjust(event_id,pays)
        
        for adjustment in result:
            self.adjustment_repo.create(adjustment)x