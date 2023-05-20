from core.entities.adjustment import Adjustment, AdjustmentId
from core.entities.user import UserId
from core.entities.event import EventId
from core.entities.friend import Friend, FriendId, Approval
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
    def create(self, friend: Friend) -> Friend:
        try:
            result = None
            request_user = UserModel.objects.get(id=friend.request_user_id)
            requested_user = UserModel.objects.get(id=friend.requested_user_id)
                        
            result = FriendModel.objects.create(
                id = friend.id,
                request_user = request_user,
                requested_user = requested_user,
                approval = friend.approval.approval,
                created_at = datetime.datetime.fromisoformat(friend.created_at)
            )
        
            return Friend.from_django_model(result)
        
        except UserModel.DoesNotExist:
            if result == None:
                return None
            result.delete()
            return None
            
    def update(self, id: FriendId, approval: Approval) -> Friend:
        try:
            result = FriendModel.objects.get(id=id)
            result.approval = approval.approval
            result.save()
            return Friend.from_django_model(result)
        
        except FriendModel.DoesNotExist:
            return None
    
    def delete(self, id: FriendId):
        pass
        """
        try:
            result = AdjustmentModel.objects.get(id=id)
            result.delete()

        except AdjustmentModel.DoesNotExist:
            pass
        """
        
    def get_by_user_id(self, user_id: UserId) -> Optional[list]:
        try:
            django_result = FriendModel.objects.filter(Q(request_user_id=user_id) | Q(requested_user_id=user_id)).order_by("created_at")
            result = [FriendModel.from_django_model(i) for i in django_result]
            return result
        
        except UserModel.DoesNotExist:
            return None
        
        except FriendModel.DoesNotExist:
            return None