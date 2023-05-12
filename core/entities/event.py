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
        
@dataclasses.dataclass(frozen=True)
class PayList:
    pay_list: list
        
#@dataclasses.dataclass(frozen=True)
#class UserIds:
    #user_ids: list

class Event:
    def __init__(self, id: EventId, name: EventName, total: AmountTotal, number_people: NumberPeople, pay_list: PayList):
        self.id = id
        self.name = name
        self.total = total
        self.number_people = number_people
        
    def adjust(self,event_id: EventId, pays: list):
        result = []
        class Record:
            def __init__(self, user_id):
                self.user_id = user_id
                self.balance = 0
        
        if pays == None:
            return None
        
        data = {}

        for item in pays:
            user_id = item.user_id
            amount_pay = item.amount_pay
            related_users = item.related_users
        
            if user_id not in data:
                data[user_id] = Record(user_id)
        
            data[user_id].balance += amount_pay #立て替えてる分を丸々支払い者に
        
            for i in related_users:
                if i not in data:
                    data[i] = Record(i)
            
                debtor = data[i] #立て替えてもらっている人(自分含む)
                cost = round(amount_pay / len(related_users))
                debtor.balance -= cost

        paid_too_much = None
        paid_less = None

        while True:
            for tbl in data.values():
                if paid_too_much is None or tbl.balance >= paid_too_much.balance:
                    paid_too_much = tbl.user_id
                if paid_less is None or tbl.balance <= paid_less.balance:
                    paid_less = tbl.user_id
                
            if paid_less.balance == 0 or paid_too_much.balance == 0:
                break

            amount = min(paid_too_much.balance, abs(paid_less.balance))
            
            adjustment_data = {
                'id': uuid.uuid4(),
                'event_id': event_id,
                'adjust_user_id': paid_too_much,
                'adjusted_user_id': paid_less,
                'amount_pay': amount,
            }
            
            result.append(adjustment_data)
            
            paid_too_much.balance -= amount
            paid_less.balance += amount
            
        return result

    @classmethod
    def from_django_model(cls, event_model: EventModel):
        return Event(
            id = event_model.id,
            name = event_model.name,
            total = event_model.total,
            number_people = event_model.number_people
            #user_ids = user_ids
        )