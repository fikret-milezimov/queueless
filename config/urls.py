from django.urls import path, include
from locations import views as location_views
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", location_views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("bookings/", include("bookings.urls")),
    path("locations/", include("locations.urls")),
]
