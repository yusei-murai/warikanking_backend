import uuid
import dataclasses
from pay.models import Pay as PayModel
from core.entities.event import EventId
from core.entities.user import UserId

@dataclasses.dataclass(frozen=True)
class PayId:
    id: uuid.UUID

@dataclasses.dataclass(frozen=True)
class PayName:
    name: str
    
@dataclasses.dataclass(frozen=True)
class AmountPay:
    amount_pay: int

class Pay:
    def __init__(self, id: PayId, name: PayName, event_id: EventId, user_id: UserId, amount_pay: AmountPay):
        self.id = id
        self.name = name
        self.event_id = event_id
        self.user_id = user_id
        self.amount_pay = amount_pay

    @classmethod
    def from_django_model(cls, pay_model: PayModel):
        return Pay(
            id = uuid.UUID(str(pay_model.id)),
            name = pay_model.name,
            event_id = pay_model.event.id,
            user_id = pay_model.user_id,
            amount_pay = pay_model.amount_pay
        )