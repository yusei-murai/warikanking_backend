import uuid

class User:
    def __init__(self, id: uuid.UUID, email: str, name: str, is_active: bool, is_staff: bool):
        self.id = id
        self.email = email
        self.name = name
        self.is_active = is_active
        self.is_staff = is_staff