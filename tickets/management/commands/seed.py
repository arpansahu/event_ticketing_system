import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tickets.models import Event

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with dummy events"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of events to seed')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        if Event.objects.exists():
            self.stdout.write(self.style.WARNING("Events already exist. Skipping seeding."))
            return

        self.stdout.write(self.style.SUCCESS(f"Seeding {count} dummy events..."))
        for _ in range(count):
            start_time = timezone.make_aware(fake.date_time_this_year(), timezone.get_current_timezone())
            end_time = timezone.make_aware(fake.date_time_this_year(), timezone.get_current_timezone())

            Event.objects.create(
                name=f"{fake.word()} Concert",
                description=fake.text(max_nb_chars=200),
                location=fake.city(),
                start_time=start_time,
                end_time=end_time,
                total_tickets=random.randint(50, 500),
                price=random.uniform(100.0, 5000.0)
            )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
