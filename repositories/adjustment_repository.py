from core.entities.adjustment import Adjustment, AdjustmentId
from core.entities.user import UserId
from core.entities.event import EventId
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from data_model.models import Adjustment as AdjustmentModel
from data_model.models  import User as UserModel
from data_model.models  import Event as EventModel
from typing import Optional
import datetime

class AdjustmentRepository(IAdjustmentRepository):
    def create(self, adjustment: Adjustment) -> Adjustment:
        try:
            event = EventModel.objects.get(id=adjustment.event_id)
            adjust_user = UserModel.objects.get(id=adjustment.adjust_user_id)
            adjusted_user = UserModel.objects.get(id=adjustment.adjusted_user_id)
            
            result = AdjustmentModel.objects.create(
                id = adjustment.id,
                event = event,
                adjust_user = adjust_user,
                adjusted_user = adjusted_user,
                amount_pay = adjustment.amount_pay,
                created_at = datetime.datetime.fromisoformat(adjustment.created_at)
            )
        
            return Adjustment.from_django_model(result)
        
        except EventModel.DoesNotExist:
            return None
        except UserModel.DoesNotExist:
            adjustments = AdjustmentModel.objects.filter(event = event)
            adjustments.delete()
            return None
        
    def create_many(self, adjustment_list: list) -> Optional[list]:
        django_results = []
        result = []
        for adjustment in adjustment_list:
            adjustment_model = AdjustmentModel(
                id = adjustment.id,
                event_id = adjustment.event_id,
                adjust_user_id = adjustment.adjust_user_id,
                adjusted_user_id = adjustment.adjusted_user_id,
                amount_pay = adjustment.amount_pay,
                created_at = datetime.datetime.fromisoformat(adjustment.created_at)
            )

            django_results.append(adjustment_model)
            result.append(Adjustment.from_django_model(adjustment_model))
                
        AdjustmentModel.objects.bulk_create(django_results)
        return result
    
    def update(self, id: AdjustmentId, adjustment: Adjustment) -> Optional[Adjustment]:
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
            AdjustmentModel.objects.select_related('event').filter(event_id=event_id).delete()

        except AdjustmentModel.DoesNotExist:
            pass
        except EventModel.DoesNotExist:
            pass
        
    def get_by_id(self, id: AdjustmentId) -> Optional[Adjustment]:
        try:
            result = AdjustmentModel.objects.get(id=id)
            return Adjustment.from_django_model(result)
        
        except AdjustmentModel.DoesNotExist:
            return None
        
    def get_by_adjust_user_id(self, user_id: UserId) -> Optional[list]:
        try:
            django_result = AdjustmentModel.objects.select_related('user').filter(adjust_user_id=user_id).order_by("created_at")
            result = [Adjustment.from_django_model(i) for i in django_result]
            return result
        except AdjustmentModel.DoesNotExist:
            return None
        
    def get_by_event_id(self, event_id: EventId) -> Optional[list]:
        try:
            django_result = AdjustmentModel.objects.select_related('event').filter(event_id=event_id).order_by("created_at")
            result = [Adjustment.from_django_model(i) for i in django_result]
            return result
        
        except AdjustmentModel.DoesNotExist:
            return None