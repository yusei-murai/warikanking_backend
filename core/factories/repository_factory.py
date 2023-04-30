from repositories.adjustment_repository import AdjustmentRepository
from repositories.user_repository import UserRepository
from repositories.event_repository import EventRepository
from repositories.pay_repository import PayRepository
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_pay_repository  import IPayRepository
from core.factories.i_repository_factory import IRepositoryFactory

class RepositoryFactory(IRepositoryFactory):
    def create_event_repository(self) -> IEventRepository:
        return EventRepository()
    
    def create_adjustment_repository(self) -> IAdjustmentRepository:
        return AdjustmentRepository()
    
    def create_pay_repository(self) -> IPayRepository:
        return PayRepository()
    
    def create_user_repository(self) -> IUserRepository:
        return UserRepository()