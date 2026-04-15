from datetime import datetime, time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking
from bookings.utils import get_available_slots
from locations.models import Location
from services_app.models import Service


class BookingLogicTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user_one = self.user_model.objects.create_user(username="user-one", password="testpass123")
        self.user_two = self.user_model.objects.create_user(username="user-two", password="testpass123")
        self.location = Location.objects.create(
            name="Central Office",
            address="1 Main St",
            city="Sofia",
            opening_time=time(9, 0),
            closing_time=time(10, 0),
        )
        self.service = Service.objects.create(
            name="Passport Renewal",
            duration_minutes=30,
            location=self.location,
        )
        self.slot = timezone.make_aware(
            datetime.combine(timezone.localdate(), time(9, 0)),
            timezone.get_current_timezone(),
        )

    def test_booked_slot_is_removed_from_available_slots(self):
        Booking.objects.create(
            user=self.user_one,
            location=self.location,
            service=self.service,
            scheduled_at=self.slot,
            status=Booking.StatusChoices.PENDING,
        )

        slots = get_available_slots(self.location, self.service, timezone.localdate())

        self.assertNotIn(self.slot, slots)

    def test_same_slot_cannot_be_booked_by_another_user(self):
        Booking.objects.create(
            user=self.user_one,
            location=self.location,
            service=self.service,
            scheduled_at=self.slot,
            status=Booking.StatusChoices.PENDING,
        )

        second_booking = Booking(
            user=self.user_two,
            location=self.location,
            service=self.service,
            scheduled_at=self.slot,
            status=Booking.StatusChoices.PENDING,
        )

        with self.assertRaises(ValidationError):
            second_booking.full_clean()
