from datetime import datetime, timedelta, time

from django.utils import timezone

from .models import Booking


def generate_time_slots(start_time, end_time, duration_minutes):
    slots = []

    current = start_time

    while current + timedelta(minutes=duration_minutes) <= end_time:
        slots.append(current)
        current += timedelta(minutes=duration_minutes)

    return slots



def get_available_slots(location, service, date):
    slot_entries = get_daily_slots(location, service, date)
    return [entry["time"] for entry in slot_entries if entry["is_available"]]


def get_daily_slots(location, service, date):
    opening_time = location.opening_time or time(9, 0)
    closing_time = location.closing_time or time(17, 0)

    current_timezone = timezone.get_current_timezone()
    start_datetime = timezone.make_aware(datetime.combine(date, opening_time), current_timezone)
    end_datetime = timezone.make_aware(datetime.combine(date, closing_time), current_timezone)

    all_slots = generate_time_slots(
        start_datetime,
        end_datetime,
        service.duration_minutes
    )

    booked_slots = Booking.objects.filter(
        location=location,
        service=service,
        scheduled_at__date=date,
        status__in=["pending", "confirmed", "in_progress"]
    ).values_list("scheduled_at", flat=True)

    booked_slots = set(booked_slots)

    return [
        {
            "time": slot,
            "is_available": slot not in booked_slots,
        }
        for slot in all_slots
    ]

