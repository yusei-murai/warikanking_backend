import uuid
import dataclasses

from pay_result.models import PayResult as PayResultModel
from core.entities.event import EventId
from core.entities.user import UserId

@dataclasses.dataclass(frozen=True)
class PayResultId:
    id: uuid.UUID
    
@dataclasses.dataclass(frozen=True)
class ResultAmountPay:
    amount_pay: int

class PayResult:
    def __init__(self, id: PayResultId, event: EventId, pay_user: UserId, paid_user: UserId, amount_pay: ResultAmountPay):
        self.id = id
        self.event = event
        self.pay_user = pay_user
        self.paid_user = paid_user
        self.amount_pay = amount_pay
        
    @classmethod
    def from_django_model(cls, pay_result_model: PayResultModel):
        return PayResult(
            id = pay_result_model.id,
            event = pay_result_model.event,
            pay_user = pay_result_model.pay_user,
            paid_user = pay_result_model.paid_user,
            amount_pay = pay_result_model.amount_pay
        )