from django.test import TestCase

from tickets.models import Event


class EventModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event.",
            location="Test Location",
            start_time="2025-02-15T18:00:00Z",
            end_time="2025-02-15T22:00:00Z",
            total_tickets=100,
            price=1000.00
        )

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.total_tickets, 100)
