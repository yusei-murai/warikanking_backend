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
        try:
            event = EventModel.objects.get(id=adjustment.event_id)
            result = AdjustmentModel.objects.create(
                id = adjustment.id,
                event = event,
                pay_user = adjustment.pay_user,
                paid_user = adjustment.paid_user,
                amount_pay = adjustment.amount_pay
            )
        
            return Adjustment.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
    
    def update(self, id: AdjustmentId, adjustment: Adjustment):
        try:
            result = AdjustmentModel.objects.get(id=id)
            result.event = EventModel.objects.get(id=adjustment.event_id)
            result.adjust_user = UserModel.objects.get(id=adjustment.adjust_user_id)
            result.adjusted_user = UserModel.objects.get(id=adjustment.adjusted_user_id)
            result.amount_pay = adjustment.amount_pay
            result.save()
            return AdjustmentModel.from_django_model(result)
        
        except AdjustmentModel.DoesNotExist:
            return None
        except UserModel.DoesNotExist:
            return None
        except EventModel.DoesNotExist:
            return None
    
    def delete(self, id: AdjustmentId):
        try:
            result = AdjustmentModel.objects.get(id=id)
            result.delete()

        except AdjustmentModel.DoesNotExist:
            pass
        
    def delete_by_event_id(self, event_id: EventId):
        try:
            event = EventModel.objects.get(id=event_id)
            AdjustmentModel.objects.filter(event=event).delete()

        except AdjustmentModel.DoesNotExist:
            pass
        except EventModel.DoesNotExist:
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