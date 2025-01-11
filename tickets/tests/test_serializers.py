from decimal import Decimal

from django.test import TestCase
from django.utils.timezone import now, timedelta

from tickets.serializers import (EventSerializer, ReportSerializer,
                                 TicketSerializer)


class EventSerializerTest(TestCase):

    def setUp(self):
        """ Set up valid event data for testing """
        future_start_time = (now() + timedelta(days=3)).isoformat()  # 3 days from today
        future_end_time = (now() + timedelta(days=3, hours=1)).isoformat()  # 1 hour after start time

        self.valid_event_data = {
            "name": "Sample Event",
            "description": "A valid event",
            "location": "Sample Location",
            "start_time": future_start_time,
            "end_time": future_end_time,
            "total_tickets": 100,
            "price": 100.00  # Valid price
        }

    def test_event_with_negative_price_fails(self):
        """ Test that an event cannot have a negative price. """
        invalid_data = self.valid_event_data.copy()
        invalid_data["price"] = -10.00  # Invalid price

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertEqual(serializer.errors['price'][0], "Price must be greater than 0.")

    def test_event_with_zero_price_fails(self):
        """ Test that an event cannot have a price of zero. """
        invalid_data = self.valid_event_data.copy()
        invalid_data["price"] = 0.00

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertEqual(serializer.errors['price'][0], "Price must be greater than 0.")

    def test_event_with_today_start_time_fails(self):
        """ Test that an event cannot start today. """
        invalid_data = self.valid_event_data.copy()
        invalid_data["start_time"] = now().isoformat()  # Today's date

        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], "An event cannot start today.")

    def test_event_with_same_day_start_and_end_time_passes(self):
        """ Test that an event can start and end on the same day. """
        valid_data = self.valid_event_data.copy()
        valid_data["end_time"] = (now() + timedelta(days=3, hours=2)).isoformat()  # Same day as start_time

        serializer = EventSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), f"Validation errors: {serializer.errors}")

    def test_valid_event_passes(self):
        """ Test that an event with valid data passes validation. """
        serializer = EventSerializer(data=self.valid_event_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Sample Event")
        self.assertEqual(serializer.validated_data["price"], Decimal("100.00"))


class TicketSerializerTest(TestCase):
    def test_ticket_serializer_contains_correct_fields(self):
        """ Test that the TicketSerializer contains the correct fields. """
        serializer = TicketSerializer()
        expected_fields = {"id", "event", "user_id", "purchase_time"}
        self.assertEqual(set(serializer.fields.keys()), expected_fields)


class ReportSerializerTest(TestCase):

    def test_valid_report_serializer_passes(self):
        """ Test that the ReportSerializer validates the report data correctly. """
        data = {
            "total_tickets_sold": 5000,
            "total_revenue": Decimal("500000.00")
        }
        serializer = ReportSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["total_tickets_sold"], 5000)
        self.assertEqual(serializer.validated_data["total_revenue"], Decimal("500000.00"))

    def test_invalid_total_tickets_sold_in_report_fails(self):
        """ Test that the ReportSerializer fails when 'total_tickets_sold' is invalid. """
        data = {
            "total_tickets_sold": "invalid",  # Invalid integer
            "total_revenue": Decimal("500000.00")
        }
        serializer = ReportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('total_tickets_sold', serializer.errors)

    def test_invalid_total_revenue_in_report_fails(self):
        """ Test that the ReportSerializer fails when 'total_revenue' is invalid. """
        data = {
            "total_tickets_sold": 5000,
            "total_revenue": "invalid"  # Invalid decimal
        }
        serializer = ReportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('total_revenue', serializer.errors)

    def test_invalid_total_tickets_and_revenue_fails(self):
        """ Test that the ReportSerializer fails when both fields are invalid. """
        data = {
            "total_tickets_sold": "invalid",
            "total_revenue": "invalid"
        }
        serializer = ReportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('total_tickets_sold', serializer.errors)
        self.assertIn('total_revenue', serializer.errors)
