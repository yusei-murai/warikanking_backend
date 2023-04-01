import uuid

class Pay:
    def __init__(self, id: uuid.UUID, name: str, event_id: uuid.UUID, user_id: uuid.UUID, amount_pay: int):
        self.id = id
        self.name = name
        self.event_id = event_id
        self.user_id = user_id
        self.amount_pay = amount_pay