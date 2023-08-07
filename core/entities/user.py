import uuid
import dataclasses
from data_model.models import User as UserModel
import re

@dataclasses.dataclass(frozen=True)
class UserId:
    id: uuid.UUID
    
@dataclasses.dataclass(frozen=True)
class Email:
    email: str
    
    def __post_init__(self):
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.email):
            raise ValueError("invalid email")
    
@dataclasses.dataclass(frozen=True)
class UserName:
    name: str
    
    def __post_init__(self):
        if len(self.name) > 20:
            raise ValueError("invalid length")

class User:
    def __init__(self, id: UserId, email: Email, name: UserName, is_active: bool, is_staff: bool):
        self.id = id
        self.email = email
        self.name = name
        self.is_active = is_active
        self.is_staff = is_staff

    @classmethod
    def from_django_model(cls, user_model: UserModel):
        return User(
            id = user_model.id,
            email = user_model.email,
            name = user_model.name,
            is_active = user_model.is_active,
            is_staff = user_model.is_staff,
        )