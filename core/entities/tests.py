import datetime
import uuid
import unittest
from unittest.mock import MagicMock,patch
from unittest.mock import Mock

from django.test import TestCase

from core.entities.event import Event, EventId
from core.entities.pay import Pay

class EventTest(TestCase):
    def setUp(self):
        self.event_id = Mock(name="EventId")

    def test_adjust(self):
        pays = [
            Pay(id="1", name="1", event_id=self.event_id, user_id="1", amount_pay="121",related_users=["1", "2", "3"],created_at=datetime.datetime.now().isoformat()),
            Pay(id="2", name="2", event_id=self.event_id, user_id="2", amount_pay="98",related_users=["1", "2", "3"],created_at=datetime.datetime.now().isoformat()),
            Pay(id="3", name="3", event_id=self.event_id, user_id="3", amount_pay="10",related_users=["1", "2", "3"],created_at=datetime.datetime.now().isoformat()),
            Pay(id="4", name="4", event_id=self.event_id, user_id="3", amount_pay="10",related_users=["1", "2"],created_at=datetime.datetime.now().isoformat()),
            Pay(id="5", name="5", event_id=self.event_id, user_id="3", amount_pay="50",related_users=["1"],created_at=datetime.datetime.now().isoformat()),
        ]
        
        with unittest.mock.patch('uuid.uuid4', return_value=uuid.UUID('ca46ddcb-0b00-46e8-b3cc-622ac98687c6')):
            success = Event.adjust(self.event_id, pays)

            expect = [
                {
                    'id': uuid.UUID('ca46ddcb-0b00-46e8-b3cc-622ac98687c6'),
                    'event_id': self.event_id,
                    'adjust_user_id': '1',
                    'adjusted_user_id': '2',
                    'amount_pay': 10,
                },
                {
                    'id': uuid.UUID('ca46ddcb-0b00-46e8-b3cc-622ac98687c6'),
                    'event_id': self.event_id,
                    'adjust_user_id': '3',
                    'adjusted_user_id': '2',
                    'amount_pay': 6,
                },
            ]

            self.assertEqual(success, expect)