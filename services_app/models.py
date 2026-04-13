from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=15)

    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE,
        related_name="services"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.location.name})"