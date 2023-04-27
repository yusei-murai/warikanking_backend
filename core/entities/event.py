import uuid
import dataclasses

from event.models import Event as EventModel

@dataclasses.dataclass(frozen=True)
class EventId:
    name: uuid.UUID

@dataclasses.dataclass(frozen=True)
class UserName:
    name: str
    
@dataclasses.dataclass(frozen=True)
class AmountTotal:
    total: int
    
@dataclasses.dataclass(frozen=True)
class NumberPeople:
    number_people: int

class Event:
    def __init__(self, id: EventId, name: UserName, total: AmountTotal, number_people: NumberPeople):
        self.id = id
        self.name = name
        self.total = total
        self.number_people = number_people

    @classmethod
    def from_django_model(cls, event_model: EventModel):
        return Event(
            id = event_model.id,
            name = event_model.name,
            total = event_model.total,
            number_people = event_model.number_people
        )