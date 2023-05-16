import uuid
import dataclasses

from data_model.models import Event as EventModel

@dataclasses.dataclass(frozen=True)
class EventId:
    name: uuid.UUID

@dataclasses.dataclass(frozen=True)
class EventName:
    name: str
        
@dataclasses.dataclass(frozen=True)
class EventCreatedAt:
    created_at: str

class Event:
    def __init__(self, id: EventId, name: EventName, created_at:EventCreatedAt):
        self.id = id
        self.name = name
        self.created_at = created_at

    @classmethod
    def adjust(cls,event_id: EventId, pays: list):
        result = []
        
        if not pays:
            return None
        
        balance = {} #user_id:balance

        for item in pays:
            user_id = item.user_id
            amount_pay = item.amount_pay
            related_users = item.related_users
        
            if user_id not in balance:
                balance[user_id] = 0
        
            balance[user_id] += amount_pay #立て替えてる分を丸々支払い者に
        
            for i in related_users:
                if i not in balance:
                    balance[i] = 0
            
                debtor = i #立て替えてもらっている人(自分含む)
                cost = round(amount_pay / len(related_users))
                balance[debtor] -= cost

        paid_too_much = None
        paid_less = None

        while True:
            for u,b in balance.items():
                if paid_too_much is None or b >= balance[paid_too_much]:
                    paid_too_much = u
                if paid_less is None or b <= balance[paid_less]:
                    paid_less = u
                
            if balance[paid_less] == 0 or balance[paid_too_much] == 0:
                break

            amount = min(balance[paid_too_much], abs(balance[paid_less]))
            
            adjustment_balance = {
                'id': uuid.uuid4(),
                'event_id': event_id,
                'adjust_user_id': paid_less,
                'adjusted_user_id': paid_too_much,
                'amount_pay': amount,
            }
            
            result.append(adjustment_balance)
            
            balance[paid_too_much]-= amount
            balance[paid_less] += amount
            
        return result

    @classmethod
    def from_django_model(cls, event_model: EventModel):
        return Event(
            id = event_model.id,
            name = event_model.name,
            created_at = event_model.created_at.isoformat()
            #user_ids = user_ids
        )