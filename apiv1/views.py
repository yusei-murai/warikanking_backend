from rest_framework import status, views  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from core.use_cases.create_pay import CreatePay
from core.use_cases.create_event import CreateEvent
from core.use_cases.get_events import GetEvents
from serializers.event_serializers import EventSerializer,RequestEventSerializer,GetRequestEventSerializer
from serializers.pay_serializers import PaySerializer,RequestPaySerializer
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository
from repositories.pay_repository import PayRepository
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.i_repositories.i_pay_repository import IPayRepository

class CreateEventAPIView(views.APIView):
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
            number_people=int(validated_data['number_people']),
            user_ids=list(validated_data['user_ids'])
        )

        serializer = EventSerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class CreatePayAPIView(views.APIView):
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
        data = request.data

        serializer = GetRequestEventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        result = usecase.get_events(validated_data['user_id'])
        print(result[0].name)
        serializer = EventSerializer(result)
        
        return Response(serializer.data, status.HTTP_200_OK)