from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import timedelta


class Booking(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No Show"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    service = models.ForeignKey(
        "services_app.Service",
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    scheduled_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if not self.scheduled_at:
            return

        # 🔥 RULE: един booking на ден за service
        existing = Booking.objects.filter(
            user=self.user,
            service=self.service,
            scheduled_at__date=self.scheduled_at.date(),
            status__in=["pending", "confirmed", "in_progress"]
        )

        if self.pk:
            existing = existing.exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError("You already have a booking for this service today.")