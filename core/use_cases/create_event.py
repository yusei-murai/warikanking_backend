from core.entities.event import Event
from core.entities.user import User
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
import uuid

class CreateEvent:
    def create_event(self,name: str,total: int,number_people: int,user_ids: list):
        users=[]

        event = Event(
            id=uuid.uuid4,
            name=name,
            total=total,
            number_people=number_people
        )
        for user_id in user_ids:
            users.append(IUserRepository.get_by_id(id=user_id))
        
        result = IEventRepository.create(event=event)
        IEventRepository.add_users_to_event(event=event,users=users)

        return result