# Create your models here.
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_tickets = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user_id = models.CharField(max_length=255)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.event.name} by {self.user_id}"
