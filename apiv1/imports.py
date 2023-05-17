import json
import uuid
import datetime

#framework
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

#entities
from core.entities.pay import Pay, AmountPay, RelatedUsers
from core.entities.event import Event, EventName
from core.entities.qr import Qr
from core.entities.friend import Friend,Approval

#use_cases
from core.use_cases.create_pay import CreatePay
from core.use_cases.create_event import CreateEvent
from core.use_cases.get_events import GetEvents
from core.use_cases.get_pays import GetPays
from core.use_cases.read_qr import ReadQr
from core.use_cases.adjust_event import AdjustmentEvent
from core.use_cases.request_friend import RequestFriend

#serializers
from serializers.event_serializers import EventSerializer, RequestEventSerializer, GetRequestEventSerializer
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