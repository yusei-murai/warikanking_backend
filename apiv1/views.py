from rest_framework import status, views  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from core.use_cases.create_pay import CreatePay
from core.use_cases.create_event import CreateEvent
from serializers.event_serializers import EventSerializer
from serializers.pay_serializers import PaySerializer
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

        result = usecase.create_event(
            name=data['name'],
            total=int(data['total']),
            number_people=int(data['number_people']),
            user_ids=list(data['user_ids'])
        )

        serializer = EventSerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class CreatePayAPIView(views.APIView):
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        pay_repo: IPayRepository = PayRepository()

        usecase = CreatePay(pay_repo)
        data = request.data

        result = usecase.create_pay(
            name=data['name'],
            event_id=data['event_id'],
            user_id=data['user_id'],
            amount_pay=int(data['amount_pay']),
        )

        serializer = PaySerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)