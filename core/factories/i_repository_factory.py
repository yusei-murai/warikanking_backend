from abc import ABC, abstractmethod
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_pay_repository import IPayRepository
from core.i_repositories.i_user_repository import IUserRepository

class IRepositoryFactory(ABC):
    @abstractmethod
    def create_event_repository(self) -> IEventRepository:
        pass
    
    @abstractmethod
    def create_pay_repository(self) -> IPayRepository:
        pass
    
    @abstractmethod
    def create_adjustment_repository(self) -> IAdjustmentRepository:
        pass
    
    @abstractmethod
    def create_user_repository(self) -> IUserRepository:
        pass