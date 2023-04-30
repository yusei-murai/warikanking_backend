from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.i_repositories.i_pay_repository import IPayRepository
from core.i_repositories.i_event_repository import IEventRepository

class AdjustmentService:
    def __init__(self, event_repo: IEventRepository, adjustment_repo: IAdjustmentRepository, pay_repo: IPayRepository):
        self.event_repo = event_repo
        self.adjustment_repo = adjustment_repo
        self.pay_repo = pay_repo
        
    def adjust(self):
        
