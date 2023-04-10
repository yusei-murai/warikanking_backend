import uuid

from event.models import Event as EventModel

class Event:
    def __init__(self, id: uuid.UUID, name: str, total: int, number_people: int):
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
