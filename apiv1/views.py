import json
import uuid
from rest_framework import status, views  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework.throttling import ScopedRateThrottle
from core.use_cases.create_pay import CreatePay
from core.use_cases.create_event import CreateEvent
from core.use_cases.get_events import GetEvents
from core.use_cases.get_pays import GetPays
from serializers.event_serializers import EventSerializer,RequestEventSerializer,GetRequestEventSerializer
from serializers.pay_serializers import PaySerializer,RequestPaySerializer,GetRequestPaySerializer
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository
from repositories.pay_repository import PayRepository
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_pay_repository import IPayRepository


class RateThrottel(ScopedRateThrottle):
    THROTTLE_RATES = {
        'create_rate': '1/second',
    }

class CreateEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        event_repo: IEventRepository = EventRepository()
        user_repo: IUserRepository = UserRepository()

        usecase = CreateEvent(event_repo, user_repo)
        data = request.data

        serializer = RequestEventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        result = usecase.create_event(
            name=validated_data['name'],
            total=int(validated_data['total']),
            user_ids=list(validated_data['user_ids'])
        )

        serializer = EventSerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class CreatePayAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        pay_repo: IPayRepository = PayRepository()

        usecase = CreatePay(pay_repo)
        data = request.data

        serializer = RequestPaySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        result = usecase.create_pay(
            name=validated_data['name'],
            event_id=validated_data['event_id'],
            user_id=validated_data['user_id'],
            amount_pay=int(validated_data['amount_pay']),
        )

        serializer = PaySerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class GetEventsAPIView(views.APIView):
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        event_repo: IEventRepository = EventRepository()

        usecase = GetEvents(event_repo)
        user_id = self.kwargs.get('user_id')
        
        try:
            user_id = uuid.UUID(user_id)
            results = usecase.get_events(user_id)
            result = [EventSerializer(i).data for i in results]
        
            return Response(result, status.HTTP_200_OK)
        except:
            return Response(result, status.HTTP_400_BAD_REQUEST)
    
class GetPaysAPIView(views.APIView):
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        pay_repo: IPayRepository = PayRepository()

        usecase = GetPays(pay_repo)
        event_id = self.kwargs.get('event_id')

        try:
            event_id = uuid.UUID(event_id)
            results = usecase.get_pays(event_id)
            result = [PaySerializer(i).data for i in results]
        
            return Response(result, status.HTTP_200_OK)
        
        except:
            return Response(result, status.HTTP_400_BAD_REQUEST)