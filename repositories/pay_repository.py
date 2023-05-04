import uuid
from typing import Optional

from core.entities.pay import Pay,PayId,RelatedUsers
from core.entities.event import EventId
from core.entities.user import UserId
from event.models import Event as EventModel
from user.models import User as UserModel
from pay.models import Pay as PayModel
from pay.models import PayRelatedUser as PayRelatedUserModel
from core.i_repositories.i_pay_repository import IPayRepository

class PayRepository(IPayRepository):
    def create(self, pay: Pay, related_users: RelatedUsers) -> Optional[Pay]:
        try:
            result = PayModel.objects.create(
                id = pay.id,
                name = pay.name,
                event_id = pay.event_id,
                user_id = pay.user_id,
                amount_pay = pay.amount_pay
            )
                        
            for user_id in related_users:
                PayRelatedUserModel.objects.create(
                    id = uuid.UUID(),
                    pay = result,
                    user_id = user_id
                )
            
            return Pay.from_django_model(result,related_users)
        
        except EventModel.DoesNotExist:
            return None
        except PayRelatedUserModel.DoesNotExist:
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
            results = PayModel.objects.filter(user__id=user_id)

            result = [Pay.from_django_model(i) for i in results]

            return result
        
        except EventModel.DoesNotExist:
            return None
        
    def get_by_event_id(self, event_id: EventId) -> Optional[list]:
        try:
            result = []
            results = PayModel.objects.filter(event__id=event_id)

            result = [Pay.from_django_model(i) for i in results]

            return result
        
        except EventModel.DoesNotExist:
            return None