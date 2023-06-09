from core.entities.event import EventId,Event
from core.entities.adjustment import Adjustment
from core.i_repositories.i_pay_repository import IPayRepository
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from django.db import transaction
import uuid
import datetime

class AdjustmentService:
    def __init__(self, pay_repo: IPayRepository, adjustment_repo: IAdjustmentRepository):
        self.pay_repo = pay_repo
        self.adjustment_repo = adjustment_repo
        
    def adjust(self, event_id: EventId):
        with transaction.atomic():
            result = []
            #self.adjustment_repo.delete_by_event_id(event_id) 元々のadjustmentを全て削除　DBに保存する場合
            pays = self.pay_repo.get_by_event_id(event_id)
            
            dict_results = Event.adjust(event_id,pays) #return->dict
            
            if dict_results == None:
                return None
            
            for dict_result in dict_results:
                adjustment = Adjustment(
                    id = dict_result['id'],
                    event_id = dict_result['event_id'],
                    adjust_user_id = dict_result['adjust_user_id'],
                    adjusted_user_id = dict_result['adjusted_user_id'],
                    amount_pay = dict_result['amount_pay'],
                    created_at = datetime.datetime.now().isoformat()
                )
                result.append(adjustment)
                
            #self.adjustment_repo.create_many(result) DBに登録する場合
            
            return result