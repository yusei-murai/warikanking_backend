from core.entities.pay import Pay,AmountPay,RelatedUsers
from core.entities.event import EventId
from core.entities.user import UserId
from core.i_repositories.i_pay_repository import IPayRepository
import uuid

class CreatePay:
    def __init__(self, pay_repo: IPayRepository):
        self.pay_repo = pay_repo

    def create_pay(self,name: str,event_id: EventId,user_id: UserId,amount_pay: AmountPay,related_users: RelatedUsers):
        pay = Pay(
            id=uuid.uuid4(),
            name=name,
            event_id=event_id,
            user_id=user_id,
            amount_pay=amount_pay,
            related_users=related_users
        )

        result = self.pay_repo.create(pay=pay)

        return result