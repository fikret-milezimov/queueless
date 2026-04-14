from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from locations.models import Location
from services_app.models import Service

from .models import Booking
from .utils import get_available_slots


def available_slots_view(request):
    location_id = request.GET.get("location")
    service_id = request.GET.get("service")

    slots = []

    if location_id and service_id:
        location = get_object_or_404(Location, id=location_id)
        service = get_object_or_404(Service, id=service_id)

        slots = get_available_slots(location, service, date.today())

    context = {
        "slots": slots
    }

    return render(request, "bookings/slots.html", context)

@login_required
def create_booking(request):
    if request.method == "POST":
        location_id = request.POST.get("location")
        service_id = request.POST.get("service")
        scheduled_at_str = request.POST.get("scheduled_at")

        location = get_object_or_404(Location, id=location_id)
        service = get_object_or_404(Service, id=service_id)

        # 🔥 parse string → datetime
        scheduled_at = datetime.fromisoformat(scheduled_at_str)
        scheduled_at = timezone.make_aware(scheduled_at)

        if not scheduled_at:
            raise ValueError("Invalid datetime format")

        booking = Booking(
            user=request.user,
            location=location,
            service=service,
            scheduled_at=scheduled_at
        )

        try:
            booking.full_clean()
        except ValidationError as exc:
            error_messages = []

            if hasattr(exc, "message_dict"):
                for messages_list in exc.message_dict.values():
                    error_messages.extend(messages_list)
            elif hasattr(exc, "messages"):
                error_messages.extend(exc.messages)
            else:
                error_messages.append(str(exc))

            for error_message in error_messages:
                messages.error(request, error_message)

            return redirect(request.META.get("HTTP_REFERER", "/"))

        booking.save()
        messages.success(request, "Booking created successfully!")

        return redirect("bookings:my-bookings")

    return redirect(request.META.get("HTTP_REFERER", "/"))




@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-scheduled_at")

    return render(request, "bookings/my-bookings.html", {
        "bookings": bookings
    })




@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.status in ["pending", "confirmed"]:
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "This booking cannot be cancelled.")

    return redirect("bookings:my-bookings")