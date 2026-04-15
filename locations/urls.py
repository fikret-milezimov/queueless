from django.urls import path

from . import views


app_name = "locations"

urlpatterns = [
    path("", views.location_list, name="list"),
    path("<int:pk>/", views.location_detail, name="detail"),
]
