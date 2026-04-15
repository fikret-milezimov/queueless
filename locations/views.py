from django.shortcuts import get_object_or_404, render

from .models import Location


def home(request):
    return render(request, "common/home.html")


def location_list(request):
    locations = Location.objects.filter(is_active=True).order_by("name")
    return render(request, "locations/location_list.html", {"locations": locations})


def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk, is_active=True)
    services = location.services.filter(is_active=True).order_by("name")
    context = {
        "location": location,
        "services": services,
    }
    return render(request, "locations/location_detail.html", context)
