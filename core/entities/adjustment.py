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
    def __init__(self, id: AdjustmentId, event_id: EventId, adjust_user_id: UserId, adjusted_user_id: UserId, amount_pay: AdjustmentAmountPay):
        self.id = id
        self.event_id = event_id
        self.adjust_user_id = adjust_user_id
        self.adjusted_user_id = adjusted_user_id
        self.amount_pay = amount_pay
        
    @classmethod
    def from_django_model(cls, adjustment_model: AdjustmentModel):
        return Adjustment(
            id = adjustment_model.id,
            event_id = adjustment_model.event.id,
            pay_user = adjustment_model.adjust_user,
            paid_user = adjustment_model.adjusted_user,
            amount_pay = adjustment_model.amount_pay
        )