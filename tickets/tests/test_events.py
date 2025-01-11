from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class EventTests(APITestCase):
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

    def test_create_event(self):
        """ Test event creation """
        response = self.client.post(self.create_event_url, self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_get_event_list(self):
        """ Test listing all events """
        self.client.post(self.create_event_url, self.event_data, format='json')
        response = self.client.get(self.create_event_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
