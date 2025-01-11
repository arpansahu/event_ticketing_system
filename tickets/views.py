from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Ticket
from .serializers import EventSerializer, ReportSerializer, TicketSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @extend_schema(
        description="List all events with pagination",
        responses={200: EventSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Event List Example",
                value=[
                    {
                        "id": 1,
                        "name": "Dua Lipa Concert",
                        "description": "A live performance by Dua Lipa.",
                        "location": "Bangalore Stadium",
                        "start_time": "2025-02-10T18:30:00Z",
                        "end_time": "2025-02-10T22:30:00Z",
                        "total_tickets": 5000,
                        "price": 5000.00
                    },
                    {
                        "id": 2,
                        "name": "Coldplay Concert",
                        "description": "A mesmerizing live performance by Coldplay.",
                        "location": "Mumbai Arena",
                        "start_time": "2025-03-15T18:00:00Z",
                        "end_time": "2025-03-15T21:00:00Z",
                        "total_tickets": 10000,
                        "price": 10000.00
                    }
                ],
                response_only=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to list all events with pagination.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Create a new event",
        request=EventSerializer,
        responses={201: EventSerializer},
        examples=[
            OpenApiExample(
                "Valid Event Creation Example",
                value={
                    "name": "The Weeknd Concert",
                    "description": "A live performance by The Weeknd with his greatest hits.",
                    "location": "Hyderabad Arena",
                    "start_time": "2025-05-10T18:00:00Z",
                    "end_time": "2025-05-10T22:00:00Z",
                    "total_tickets": 3000,
                    "price": 7000.00
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new event.
        """
        return super().post(request, *args, **kwargs)


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @extend_schema(
        description="Retrieve details of a specific event by ID",
        responses={200: EventSerializer},
        examples=[
            OpenApiExample(
                "Event Detail Example",
                value={
                    "id": 1,
                    "name": "Dua Lipa Concert",
                    "description": "A live performance by Dua Lipa.",
                    "location": "Bangalore Stadium",
                    "start_time": "2025-02-10T18:30:00Z",
                    "end_time": "2025-02-10T22:30:00Z",
                    "total_tickets": 5000,
                    "price": 5000.00
                },
                response_only=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve event details.
        """
        event = self.get_object()

        # Check if the event has already ended
        if event.end_time < now():
            return Response(self.get_serializer(event).data)  # Respond without caching logic

        return super().retrieve(request, *args, **kwargs)


class TicketPurchaseView(generics.CreateAPIView):
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles ticket purchase requests for an event.
        """
        event_id = request.data.get('event')
        user_id = request.data.get('user_id')

        try:
            with transaction.atomic():
                event = Event.objects.select_for_update().get(id=event_id)
                if event.total_tickets <= 0:
                    return Response({"error": "Tickets sold out!"}, status=status.HTTP_400_BAD_REQUEST)

                # Atomically decrement total tickets
                event.total_tickets = F('total_tickets') - 1
                event.save()

                ticket = Ticket.objects.create(event=event, user_id=user_id)
                return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)

        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


class ReportView(APIView):
    @extend_schema(
        description="Get the total number of tickets sold and total revenue",
        responses={200: ReportSerializer},  # Use ReportSerializer for OpenAPI documentation
    )

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to return a report of ticket sales and revenue.
        """
        total_tickets_sold = Ticket.objects.count()  # Total number of tickets sold
        total_revenue = sum(ticket.event.price for ticket in Ticket.objects.all())  # Sum of all ticket prices

        # Serialize the data using ReportSerializer
        data = {
            "total_tickets_sold": total_tickets_sold,
            "total_revenue": total_revenue,
        }
        serializer = ReportSerializer(data)

        return Response(serializer.data)