from core.entities.event import Event
from core.entities.user import User
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
import uuid

class CreateEvent:
    def __init__(self, event_repo: IEventRepository, user_repo: IUserRepository):
        self.event_repo = event_repo
        self.user_repo = user_repo

    def create_event(self,name: str,total: int,number_people: int,user_ids: list):
        users=[]

        event = Event(
            id=uuid.uuid4(),
            name=name,
            total=total,
            number_people=number_people
        )

        for user_id in user_ids:
            users.append(self.user_repo.get_by_id(id=user_id))

        result = self.event_repo.create(event=event)
        self.event_repo.add_users_to_event(event=event,users=users)

        return result