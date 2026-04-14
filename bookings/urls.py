from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("slots/", views.available_slots_view, name="slots"),
    path("create/", views.create_booking, name="create"),
    path("my/", views.my_bookings, name="my-bookings"),
    path("cancel/<int:pk>/", views.cancel_booking, name="cancel-booking"),
]