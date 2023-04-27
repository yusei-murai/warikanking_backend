import uuid
import dataclasses
from user.models import User as UserModel

@dataclasses.dataclass(frozen=True)
class UserId:
    id: uuid.UUID
    
@dataclasses.dataclass(frozen=True)
class Email:
    email: str
    
@dataclasses.dataclass(frozen=True)
class UserName:
    name: str

class User:
    def __init__(self, id: uuid.UUID, email: Email, name: UserName, is_active: bool, is_staff: bool):
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