from core.entities.adjustment import Adjustment, AdjustmentId
from core.entities.user import UserId
from core.entities.event import EventId
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from adjustment.models import Adjustment as AdjustmentModel
from user.models import User as UserModel
from event.models import Event as EventModel
from typing import Optional

class AdjustmentRepository(IAdjustmentRepository):
    def create(self, adjustment: Adjustment):
        result = AdjustmentModel.objects.create(
            id = adjustment.id,
            event = adjustment.event,
            pay_user = adjustment.pay_user,
            paid_user = adjustment.paid_user,
            amount_pay = adjustment.amount_pay
        )
        
        return Adjustment.from_django_model(result)
    
    def update(self, id: AdjustmentId, adjustment: Adjustment):
        try:
            result = AdjustmentModel.objects.get(id=id)
            result.event = adjustment.event
            result.adjust_user = adjustment.adjust_user
            result.adjusted_user = adjustment.adjusted_user
            result.amount_pay = adjustment.amount_pay
            result.save()
            return AdjustmentModel.from_django_model(result)
        
        except AdjustmentModel.DoesNotExist:
            return None
    
    def delete(self, id: AdjustmentId):
        try:
            result = AdjustmentModel.objects.get(id=id)
            result.delete()

        except AdjustmentModel.DoesNotExist:
            pass
        
    def get_by_id(self, id: AdjustmentId):
        try:
            result = AdjustmentModel.objects.get(id=id)
            return Adjustment.from_django_model(result)
        
        except AdjustmentModel.DoesNotExist:
            return None
        
    def get_by_adjustuser_id(self, user_id: UserId):
        try:
            adjust_user = UserModel.objects.get(id=user_id)
            django_result = AdjustmentModel.objects.filter(adjust_user=adjust_user)
            result = [Adjustment.from_django_model(i) for i in django_result]
            return result
        except AdjustmentModel.DoesNotExist:
            return None
        
    def get_by_event_id(self, event_id: EventId):
        try:
            event = EventModel.objects.get(id=event_id)
            django_result = AdjustmentModel.objects.filter(event=event)
            result = [Adjustment.from_django_model(i) for i in django_result]
            return result
        except AdjustmentModel.DoesNotExist:
            return None