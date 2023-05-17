from core.entities.adjustment import Adjustment, AdjustmentId
from core.entities.user import UserId
from core.entities.event import EventId
from core.entities.friend import Friend, FriendId
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.i_repositories.i_friend_repository import IFriendRepository
from data_model.models import Adjustment as AdjustmentModel
from data_model.models  import User as UserModel
from data_model.models  import Event as EventModel
from data_model.models  import Friend as FriendModel
from typing import Optional
import datetime
from django.db.models import Q

class FriendRepository(IFriendRepository):
    def create(self, friend: Friend):
        try:
            result = None
            user_1 = UserModel.objects.get(id=friend._user_id)
            user_2 = UserModel.objects.get(id=friend.adjusted_user_id)
            
            result = FriendModel.objects.create(
                id = friend.id,
                user_1 = user_1,
                user_2 = user_2,
                approval = friend.approval,
                created_at = datetime.datetime.fromisoformat(friend.created_at)
            )
        
            return Adjustment.from_django_model(result)
        
        except UserModel.DoesNotExist:
            if result == None:
                return None
            result.delete()
            return None
            
    def update(self, id: AdjustmentId, adjustment: Adjustment):
        pass
        """
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
        """
    
    def delete(self, id: AdjustmentId):
        pass
        """
        try:
            result = AdjustmentModel.objects.get(id=id)
            result.delete()

        except AdjustmentModel.DoesNotExist:
            pass
        """
        
    def get_by_user_id(self, user_id: UserId):
        try:
            user = UserModel.objects.get(id=user_id)
            django_result = FriendModel.objects.filter(Q(user_1=user)|Q(user_2=user)).order_by("created_at")
            result = [FriendModel.from_django_model(i) for i in django_result]
            return result
        
        except UserModel.DoesNotExist:
            return None
        
        except FriendModel.DoesNotExist:
            return None