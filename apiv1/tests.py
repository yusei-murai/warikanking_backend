from django.test import TestCase
from rest_framework import status
from unittest import mock
from django.urls import reverse
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository
from repositories.pay_repository import PayRepository
from core.i_repositories.i_event_repository import IEventRepository
from core.i_repositories.i_user_repository import IUserRepository
from core.use_cases.create_event import CreateEvent
from core.entities.event import Event
from core.entities.user import User

class testCreateEventAPIView(TestCase):
    def setUp(self):
        self.url = reverse('apiv1:create-event')
        self.event_repo_mock = mock.create_autospec(IEventRepository)
        self.user_repo_mock = mock.create_autospec(IUserRepository)
        self.usecase = CreateEvent(self.event_repo_mock, self.user_repo_mock)

    @mock.patch('repositories.event_repository.EventRepository')
    @mock.patch('repositories.user_repository.UserRepository')
    @mock.patch('core.use_cases.create_event.CreateEvent')
    def test_create_event(self,mockedEventRepository,mockedUserRepository,mockedCreateEvent):
        mock_event_repo = mock.Mock()
        mock_create_event_usecase = mock.Mock()

        mock_event_repo.create.return_value = Event(id="12c7be59-1b7c-40a4-bda0-34793282dc77", name='test_event', total=10, number_people=3)
        mock_event_repo.add_users_to_event.return_value = Event(id="12c7be59-1b7c-40a4-bda0-34793282dc77", name='test_event', total=10, number_people=3)
        mock_create_event_usecase.createEvent.return_value = Event(id="12c7be59-1b7c-40a4-bda0-34793282dc77", name='test_event', total=10, number_people=3)
        mockedEventRepository.return_value = mock_event_repo
        mockedCreateEvent.return_value = mock_create_event_usecase

        data = {
            "id": "12c7be59-1b7c-40a4-bda0-34793282dc77",
            "name": "fcfc",
            "total": 11,
            "user_ids":["12c7be59-1b7c-40a4-bda0-34793282dc77",]
        }
        
        serializer_data = {
            "name" : "fcfc",
            "total" : 11,
            "user_ids" : ["12c7be59-1b7c-40a4-bda0-34793282dc77",]
        }
        
        with mock.patch('serializers.event_serializers.RequestEventSerializer') as serializer_mock:
            serializer_mock.return_value.is_valid.return_value = True
            serializer_mock.return_value.validated_data = serializer_data
            response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)