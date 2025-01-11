from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class TicketTests(APITestCase):
    def setUp(self):
        self.event_data = {
            "name": "Sample Event",
            "description": "A test event.",
            "location": "Test Location",
            "start_time": "2025-02-15T18:00:00Z",
            "end_time": "2025-02-15T22:00:00Z",
            "total_tickets": 5,
            "price": 100.00
        }
        self.create_event_url = reverse('event-list-create')
        self.purchase_ticket_url = reverse('ticket-purchase')
        response = self.client.post(self.create_event_url, self.event_data, format='json')
        self.event_id = response.data['id']

    def test_ticket_purchase_success(self):
        """ Test successful ticket purchase """
        ticket_data = {
            "event": self.event_id,
            "user_id": "test_user"
        }
        response = self.client.post(self.purchase_ticket_url, ticket_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_ticket_purchase_sold_out(self):
        """ Test purchase when tickets are sold out """
        for i in range(5):
            self.client.post(self.purchase_ticket_url, {"event": self.event_id, "user_id": f"user_{i}"}, format='json')

        response = self.client.post(self.purchase_ticket_url, {"event": self.event_id, "user_id": "late_user"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Tickets sold out!")

    def test_event_not_found(self):
        """ Test ticket purchase for non-existent event """
        ticket_data = {
            "event": 99999,
            "user_id": "user1"
        }
        response = self.client.post(self.purchase_ticket_url, ticket_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Event not found")
