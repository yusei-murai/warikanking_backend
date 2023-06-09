from core.entities.event import Event,EventId
from core.entities.user import User
from core.entities.pay import Pay
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_pay_repository import IPayRepository
import uuid

class GetPays:
    def __init__(self, pay_repo: IPayRepository):
        self.pay_repo = pay_repo

    def get_pays(self,event_id: EventId):
        result = self.pay_repo.get_by_event_id(event_id)

        return result