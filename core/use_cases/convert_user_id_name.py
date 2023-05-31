from core.entities.event import Event, EventName
from core.entities.user import User, UserId
from core.entities.friend import Friend, Approval, FriendId
from core.services.user_service import UserService
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_friend_repository import IFriendRepository
from core.factories.repository_factory import RepositoryFactory
import uuid


class ConvertUserIdName:
    def convert_user_id_name(self, user_id: UserId):
        factory = RepositoryFactory()
        user_repo: IUserRepository = factory.create_user_repository()
        service = UserService(user_repo)

        result = service.convert_user_id_name(user_id)

        return result
