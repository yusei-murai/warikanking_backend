from core.entities.pay import Pay
from core.i_repositories.i_pay_repository import IPayRepository
import uuid

class CreatePay:
    def __init__(self, pay_repo: IPayRepository):
        self.pay_repo = pay_repo

    def create_pay(self,name: str,event_id: uuid.UUID,user_id: uuid.UUID,amount_pay: int):
        pay = Pay(
            id=uuid.uuid4(),
            name=name,
            event_id=event_id,
            user_id=user_id,
            amount_pay=amount_pay
        )

        result = self.pay_repo.create(pay=pay)

        return result