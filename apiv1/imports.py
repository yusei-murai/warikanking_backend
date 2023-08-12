import json
import uuid
import datetime

#framework
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

#entities
from core.entities.pay import Pay, AmountPay, RelatedUsers, PayName, PayId
from core.entities.event import Event, EventName, EventId, IsConfirmed
from core.entities.qr import Qr, QrId
from core.entities.friend import Friend,Approval, FriendId
from core.entities.user import User, UserId

#services
from core.services.user_service import UserService

#use_cases
from core.use_cases.create_pay import CreatePay
from core.use_cases.create_event import CreateEvent
from core.use_cases.get_event import GetEvent
from core.use_cases.get_events import GetEvents
from core.use_cases.get_pays import GetPays
from core.use_cases.read_qr import ReadQr
from core.use_cases.adjust_event import AdjustmentEvent
from core.use_cases.request_friend import RequestFriend
from core.use_cases.approve_friend import ApproveFriend
from core.use_cases.get_friends import GetFriends
from core.use_cases.convert_user_id_name import ConvertUserIdName
from core.use_cases.get_users_dict_by_event import GetUsersDictByEventId
from core.use_cases.add_users_event import AddUsersEvent
from core.use_cases.confirm_event import ConfirmEvent

#serializers
from serializers.event_serializers import EventSerializer, RequestEventSerializer, GetRequestEventSerializer, AddUsersEventSerializer
from serializers.pay_serializers import PaySerializer, RequestPaySerializer, GetRequestPaySerializer
from serializers.friend_serializers import RequestFriendSerializer

#i_repositories
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_pay_repository import IPayRepository
from core.i_repositories.i_adjustment_repository import IAdjustmentRepository
from core.i_repositories.i_friend_repository import IFriendRepository

#factories
from core.factories.repository_factory import RepositoryFactory