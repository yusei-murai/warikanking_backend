from rest_framework import status, views  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from core.use_cases.create_event import CreateEvent
from serializers.event_serializers import EventSerializer
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository


import uuid

class CreateEventAPIView(views.APIView):
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        usecase = CreateEvent(EventRepository, UserRepository)
        data = request.data

        result = usecase.create_event(
            name=data['name'],
            total=int(data['total']),
            number_people=int(data['number_people']),
            user_ids=list(data['user_ids'])
        )

        serializer = EventSerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)