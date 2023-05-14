from core.factories.repository_factory import RepositoryFactory
from core.i_repositories.i_pay_repository import IPayRepository
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.entities.event import EventId
from core.services.adjustment_service import AdjustmentService
        
class AdjustmentEvent:     
    def adjust_event(self,event_id: EventId):
        factory = RepositoryFactory()
        pay_repo: IPayRepository = factory.create_pay_repository()
        adjustment_repo: IAdjustmentRepository = factory.create_adjustment_repository()
        
        service = AdjustmentService(pay_repo,adjustment_repo)

        return service.adjust(event_id)