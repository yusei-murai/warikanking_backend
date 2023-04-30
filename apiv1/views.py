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
from core.entities.event import Event
from serializers.event_serializers import EventSerializer,RequestEventSerializer,GetRequestEventSerializer
from serializers.pay_serializers import PaySerializer,RequestPaySerializer,GetRequestPaySerializer
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_pay_repository import IPayRepository
from core.factories.repository_factory import RepositoryFactory

class RateThrottel(ScopedRateThrottle):
    THROTTLE_RATES = {
        'create_rate': '1/second',
    }

class CreateEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        event_repo: IEventRepository = factory.create_event_repository()
        user_repo: IUserRepository = factory.create_user_repository()

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
        
        if type(result) is str:
            message = json.dumps({"message":result},ensure_ascii=False)
            return Response(message, status.HTTP_400_BAD_REQUEST)
            
        else:
            serializer = EventSerializer(result)
            
            return Response(serializer.data, status.HTTP_201_CREATED)
    
class CreatePayAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        pay_repo: IPayRepository = factory.create_pay_repository()

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
        factory = RepositoryFactory()
        event_repo: IEventRepository = factory.create_event_repository()

        usecase = GetEvents(event_repo)
        user_id = self.kwargs.get('user_id')
        
        try:
            user_id = uuid.UUID(user_id)
            results = usecase.get_events(user_id)
            
            result = [EventSerializer(i).data for i in results]
            
            if not result:
                return Response(result, status.HTTP_204_NO_CONTENT)
        
            return Response(result, status.HTTP_200_OK)
        except:
            return Response(json.dumps({"message":"failed"}), status.HTTP_400_BAD_REQUEST)
    
class GetPaysAPIView(views.APIView):
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        pay_repo: IPayRepository = factory.create_pay_repository()

        usecase = GetPays(pay_repo)
        event_id = self.kwargs.get('event_id')

        try:
            event_id = uuid.UUID(event_id)
            results = usecase.get_pays(event_id)
            result = [PaySerializer(i).data for i in results]
            
            if not result:
                return Response(result, status.HTTP_204_NO_CONTENT)
        
            return Response(result, status.HTTP_200_OK)
        
        except:
            return Response(result, status.HTTP_400_BAD_REQUEST)