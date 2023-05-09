from core.entities.event import EventId
from core.entities.adjustment import Adjustment
import uuid

class AdjustmentService:   
    def adjust(event_id: EventId,pays: list):
        result = []
        class Record:
            def __init__(self, name):
                self.name = name
                self.balance = 0
        
        if pays == None:
            return None
        
        data = {}

        for item in pays:
            user_id = item["user_id"]
            amount_pay = item["amount_pay"]
            related_users = item["related_users"]
        
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
                    paid_too_much = tbl
                if paid_less is None or tbl.balance <= paid_less.balance:
                    paid_less = tbl
                
            if paid_less.balance == 0 or paid_too_much.balance == 0:
                break

            amount = min(paid_too_much.balance, abs(paid_less.balance))
            
            adjustment = Adjustment(
                id = uuid.uuid4(),
                event_id = event_id,
                adjust_user_id = paid_too_much,
                adjusted_user_id = paid_less,
                amount_pay = amount,
            )
            
            result.append(adjustment)
            
            paid_too_much.balance -= amount
            paid_less.balance += amount
            
        return result