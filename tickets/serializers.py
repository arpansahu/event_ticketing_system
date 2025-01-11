
from django.utils.timezone import now
from rest_framework import serializers

from .models import Event, Ticket
from datetime import timedelta
from django.utils.timezone import now




class EventSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Event
        fields = '__all__'

    def validate_price(self, value):
        """ Ensure price is greater than 0. """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, data):
        """ Ensure the event does not start today but can end on the same day. """
        start_time = data['start_time']
        if start_time.date() == now().date():
            raise serializers.ValidationError("An event cannot start today.")
        if data['end_time'] < data['start_time']:
            raise serializers.ValidationError("End time cannot be before start time.")
        return data

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class ReportSerializer(serializers.Serializer):
    total_tickets_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)