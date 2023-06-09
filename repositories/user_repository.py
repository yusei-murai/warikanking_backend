import uuid
from typing import Optional

from core.entities.user import User,UserId
from core.entities.event import EventId
from data_model.models import Event as EventModel
from data_model.models import User as UserModel
from data_model.models import Friend as FriendModel
from core.i_repositories.i_user_repository import IUserRepository

class UserRepository(IUserRepository):
    def get_by_id(self, id: UserId) -> Optional[User]:
        try:
            result = UserModel.objects.get(id=id)
            return User.from_django_model(result)
        
        except UserModel.DoesNotExist:
            return None
        
    def get_users_by_ids(self, user_ids: list) -> Optional[list]:
        try:
            result = [User.from_django_model(user) for user in UserModel.objects.filter(id__in=user_ids)]
            return result
        
        except UserModel.DoesNotExist:
            return None
    
    def get_all_by_event_id(self, event_id: EventId) -> Optional[list]:
        try:
            result = []
            event = EventModel.objects.prefetch_related('users').get(id=event_id)
            users = event.users.all()

            result = [User.from_django_model(user) for user in users]

            return result
        except EventModel.DoesNotExist as e:
            return None