from rest_framework import status, views  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from core.use_cases.create_event import CreateEvent
import uuid

class CreateEventAPIView(views.APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        usecase = CreateEvent()
        data = request.data

        result = usecase.create_event(
            name=data['name'],
            total=int(data['total']),
            number_people=int(data['number_people']),
            user_ids=list(data['user_ids'])
            )
        
        return Response(result, status.HTTP_201_CREATED)