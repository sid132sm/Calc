import uuid

from django.db import models


class Calculation(models.Model):
    """Persisted calculation history; evaluation is implemented in a later phase."""

    class AngleMode(models.TextChoices):
        DEGREES = "deg", "Degrees"
        RADIANS = "rad", "Radians"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.UUIDField(db_index=True)
    expression = models.TextField()
    normalized_expression = models.TextField(blank=True)
    result = models.TextField()
    angle_mode = models.CharField(max_length=3, choices=AngleMode, default=AngleMode.DEGREES)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["device_id", "-created_at"],
                name="calculator__device__c758ff_idx",
            )
        ]
