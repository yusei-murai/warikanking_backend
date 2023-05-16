import uuid
from typing import Optional
import datetime

from core.entities.pay import Pay,PayId,RelatedUsers
from core.entities.event import EventId
from core.entities.user import UserId
from data_model.models  import Event as EventModel
from data_model.models  import User as UserModel
from data_model.models  import Pay as PayModel
from data_model.models  import PayRelatedUser as PayRelatedUserModel
from core.i_repositories.i_pay_repository import IPayRepository

class PayRepository(IPayRepository):
    def create(self, pay: Pay) -> Optional[Pay]:
        try:
            result = None
            
            user = UserModel.objects.get(id = pay.user_id)
            event = EventModel.objects.get(id = pay.event_id)
            result = PayModel.objects.create(
                id = pay.id,
                name = pay.name,
                event = event,
                user = user,
                amount_pay = pay.amount_pay,
                created_at = datetime.datetime.fromisoformat(pay.created_at)
            )
                 
            for user_id in pay.related_users:
                user = UserModel.objects.get(id=user_id)
                PayRelatedUserModel.objects.create(
                    id = uuid.uuid4(),
                    pay = result,
                    user = user,
                    created_at = result.created_at
                )
            
            return Pay.from_django_model(result,pay.related_users)
        
        except EventModel.DoesNotExist:
            if result == None:
                return None
            result.delete()
            return None
        
        except PayRelatedUserModel.DoesNotExist:
            if result == None:
                return None
            result.delete()
            return None
        
        except UserModel.DoesNotExist:
            if result == None:
                return None
            result.delete()
            return None
    
    def update(self, id: PayId, new_pay: Pay, related_users: RelatedUsers) -> Optional[Pay]:
        try:
            result = PayModel.objects.get(id=id)
            result.name = new_pay.name
            result.user = UserModel.objects.get(id=new_pay.user_id)
            result.amount_pay = new_pay.amount_pay
            result.save()
            #未完成
            #related_users_results = [PayRelatedUserModel.objects.get(result.user_id = result) for result in related_users]
            return PayModel.from_django_model(result)
        
        except PayModel.DoesNotExist:
            return None
        
        except EventModel.DoesNotExist:
            return None
        
    def delete(self, id: PayId):
        try:
            result = PayModel.objects.get(id=id)
            result.delete()

        except PayModel.DoesNotExist:
            pass
    
    def get_by_id(self, id: PayId) -> Optional[Pay]:
        try:
            result = PayModel.objects.get(id=id)
            return Pay.from_django_model(result)
        
        except PayModel.DoesNotExist:
            return None
        
    def get_by_user_id(self, user_id: UserId) -> Optional[list]:
        try:
            result = []
            results = PayModel.objects.filter(user__id=user_id).order_by("created_at")

            for i in results:
                pay_users = PayRelatedUserModel.objects.filter(pay__id=i.id).order_by("created_at")
                pay_users_ids = [i.id for i in pay_users]
                result.append(Pay.from_django_model(i,pay_users_ids))

            return result
        
        except EventModel.DoesNotExist:
            return None
        
    def get_by_event_id(self, event_id: EventId) -> Optional[list]:
        try:
            result = []
            results = PayModel.objects.filter(event__id=event_id)
            
            for i in results:
                pay_users = PayRelatedUserModel.objects.filter(pay__id=i.id).order_by("created_at")
                pay_users_ids = [i.user.id for i in pay_users]
                result.append(Pay.from_django_model(i,pay_users_ids))

            return result
        
        except EventModel.DoesNotExist:
            return None