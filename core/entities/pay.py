import uuid
from pay.models import Pay as PayModel

class Pay:
    def __init__(self, id: uuid.UUID, name: str, event_id: uuid.UUID, user_id: uuid.UUID, amount_pay: int):
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
            user_id = uuid.UUID(pay_model.user_id),
            amount_pay = pay_model.amount_pay
        )