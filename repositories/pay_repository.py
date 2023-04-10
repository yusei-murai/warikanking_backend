import uuid
from typing import Optional

from core.entities.pay import Pay
from event.models import Event as EventModel
from user.models import User as UserModel
from pay.models import Pay as PayModel
from core.i_repositories.i_pay_repository import IPayRepository

class PayRepository(IPayRepository):
    def create(self, pay: Pay) -> Optional[Pay]:
        try:
            result = PayModel.objects.create(
                id = pay.id,
                name = pay.name,
                event_id = pay.event_id,
                user_id = pay.user_id,
                amount_pay = pay.amount_pay
            )

            return Pay.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
    
    def update(self, id: uuid.UUID, pay: Pay) -> Optional[Pay]:
        try:
            result = PayModel.objects.get(id=id)
            result.name = pay.name
            result.user = UserModel.objects.get(id=pay.user_id),
            result.event = EventModel.objects.get(id=pay.event_id),
            result.amount_pay = pay.amount_pay
            result.save()
            return PayModel.from_django_model(result)
        
        except PayModel.DoesNotExist:
            return None
        
        except EventModel.DoesNotExist:
            return None
        
    def delete(self, id: uuid.UUID):
        try:
            result = PayModel.objects.get(id=id)
            result.delete()

        except PayModel.DoesNotExist:
            pass
    
    def get_by_id(self, id: uuid.UUID) -> Optional[Pay]:
        try:
            result = PayModel.objects.get(id=id)
            return Pay.from_django_model(result)
        
        except PayModel.DoesNotExist:
            return None
        
    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[list]:
        try:
            result = []
            results = PayModel.objects.filter(user__id=user_id)

            result = [Pay.from_django_model(i) for i in results]

            return result
        
        except EventModel.DoesNotExist:
            return None
        
    def get_by_event_id(self, event_id: uuid.UUID) -> Optional[list]:
        try:
            result = []
            results = PayModel.objects.filter(event__id=event_id)

            result = [Pay.from_django_model(i) for i in results]

            return result
        
        except EventModel.DoesNotExist:
            return None