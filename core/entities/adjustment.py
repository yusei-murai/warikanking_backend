import uuid
import dataclasses

from adjustment.models import Adjustment as AdjustmentModel
from core.entities.event import EventId
from core.entities.user import UserId

@dataclasses.dataclass(frozen=True)
class AdjustmentId:
    id: uuid.UUID
    
@dataclasses.dataclass(frozen=True)
class AdjustmentAmountPay:
    amount_pay: int

class Adjustment:
    def __init__(self, id: AdjustmentId, event: EventId, adjust_user: UserId, adjusted_user: UserId, amount_pay: AdjustmentAmountPay):
        self.id = id
        self.event = event
        self.pay_user = adjust_user
        self.paid_user = adjusted_user
        self.amount_pay = amount_pay
        
    @classmethod
    def from_django_model(cls, adjustment_model: AdjustmentModel):
        return Adjustment(
            id = adjustment_model.id,
            event = adjustment_model.event,
            pay_user = adjustment_model.adjust_user,
            paid_user = adjustment_model.adjusted_user,
            amount_pay = adjustment_model.amount_pay
        )