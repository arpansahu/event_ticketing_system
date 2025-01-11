import threading
from datetime import timedelta

from django.db import connection
from django.test import Client, TransactionTestCase
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status


class ConcurrentTicketPurchaseTest(TransactionTestCase):
    reset_sequences = True  # Ensure primary keys start from 1

    def setUp(self):
        random_days_in_future = 3  # Ensure the event is in the future
        self.event_data = {
            "name": "Sample Event",
            "description": "A test event.",
            "location": "Test Location",
            "start_time": (now() + timedelta(days=random_days_in_future)).isoformat(),
            "end_time": (now() + timedelta(days=random_days_in_future, hours=1)).isoformat(),
            "total_tickets": 5,
            "price": 100.00
        }
        self.create_event_url = reverse('event-list-create')
        self.purchase_ticket_url = reverse('ticket-purchase')

        response = self.client.post(self.create_event_url, self.event_data, format='json')
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Event creation failed: {response.data}")
        self.event_id = response.data.get('id')

    def purchase_ticket_thread(self, user_id, result_list):
        """
        Thread function to simulate ticket purchase request.
        """
        thread_client = Client()  # Create a new client per thread to avoid shared state
        try:
            response = thread_client.post(self.purchase_ticket_url, {
                "event": self.event_id,
                "user_id": user_id
            }, format='json')
            result_list.append(response.status_code)
        finally:
            # Close connection to avoid database locks
            connection.close()

    def test_concurrent_ticket_purchases(self):
        """
        Test concurrent ticket purchases to ensure atomic transactions.
        """
        num_threads = 10  # 10 concurrent requests
        threads = []
        results = []

        # Create and start threads
        for i in range(num_threads):
            thread = threading.Thread(target=self.purchase_ticket_thread, args=(f"user_{i}", results))
            threads.append(thread)
            thread.start()

        # Join all threads
        for thread in threads:
            thread.join()

        successful_purchases = results.count(status.HTTP_201_CREATED)
        failed_purchases = results.count(status.HTTP_400_BAD_REQUEST)

        # Assert only 5 successful purchases and the rest failed
        self.assertEqual(successful_purchases, 5, f"Expected 5 successful purchases, got {successful_purchases}")
        self.assertEqual(failed_purchases, num_threads - 5, f"Expected {num_threads - 5} failed purchases, got {failed_purchases}")
