from core.entities.pay import Pay,AmountPay,RelatedUsers
from core.entities.event import EventId
from core.entities.user import UserId
from core.i_repositories.i_pay_repository import IPayRepository
import uuid

class CreatePay:
    def __init__(self, pay_repo: IPayRepository):
        self.pay_repo = pay_repo

    def create_pay(self,pay: Pay):
        result = self.pay_repo.create(pay=pay)

        return result