import uuid

class Event:
    def __init__(self, id: uuid.UUID, name: str, total: int, number_people: int):
        self.id = id
        self.name = name
        self.total = total
        self.number_people = number_people