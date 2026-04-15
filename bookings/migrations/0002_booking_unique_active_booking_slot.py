from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.UniqueConstraint(
                condition=Q(status__in=["pending", "confirmed", "in_progress"]),
                fields=("location", "service", "scheduled_at"),
                name="unique_active_booking_slot",
            ),
        ),
    ]
