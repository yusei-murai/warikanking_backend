import uuid
import dataclasses

from event.models import Event as EventModel

@dataclasses.dataclass(frozen=True)
class EventId:
    name: uuid.UUID

@dataclasses.dataclass(frozen=True)
class EventName:
    name: str
    
@dataclasses.dataclass(frozen=True)
class AmountTotal:
    total: int
    
@dataclasses.dataclass(frozen=True)
class NumberPeople:
    number_people: int
    
    def __post_init__(self):
        if self.number_people < 2:
            raise ValueError("shortage people")
        
#@dataclasses.dataclass(frozen=True)
#class UserIds:
    #user_ids: list

class Event:
    def __init__(self, id: EventId, name: EventName, total: AmountTotal, number_people: NumberPeople):
        self.id = id
        self.name = name
        self.total = total
        self.number_people = number_people

    @classmethod
    def from_django_model(cls, event_model: EventModel,):
        return Event(
            id = event_model.id,
            name = event_model.name,
            total = event_model.total,
            number_people = event_model.number_people
            #user_ids = user_ids
        )