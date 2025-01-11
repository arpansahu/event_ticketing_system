from django.urls import path

from tickets.views import (EventDetailView, EventListCreateView, ReportView,
                           TicketPurchaseView)

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('tickets/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
    path('reports/', ReportView.as_view(), name='report'),
]
