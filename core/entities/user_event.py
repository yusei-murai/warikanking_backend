import uuid

class UserEvent:
    def __init__(self, id: uuid.UUID,  event_id: uuid.UUID, user_id: uuid.UUID):
        self.id = id
        self.event_id = event_id
        self.user_id = user_id