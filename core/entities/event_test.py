import unittest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath("."))
from core.entities.event import Event, EventId
from core.entities.pay import Pay

class EventTest(unittest.TestCase):
    def test_adjust(self):
        event_id = EventId("example_event_id")
        pays = [
            Pay(user_id="user1", amount_pay=30, related_users=["user2", "user3"]),
            Pay(user_id="user2", amount_pay=20, related_users=["user1"]),
            Pay(user_id="user3", amount_pay=10, related_users=["user1"]),
        ]

        success_result = Event.adjust(event_id, pays)
        empty_result = Event.adjust(event_id, [])

        expected_result = [
            {
                'id': MagicMock(),
                'event_id': event_id,
                'adjust_user_id': 'user3',
                'adjusted_user_id': 'user1',
                'amount_pay': 5,
            },
            {
                'id': MagicMock(),
                'event_id': event_id,
                'adjust_user_id': 'user2',
                'adjusted_user_id': 'user1',
                'amount_pay': 5,
            },
        ]

        self.assertEqual(success_result, expected_result)

if __name__ == '__main__':
    unittest.main()