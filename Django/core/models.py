from django.db import models
from django.utils.timezone import now
# Create your models here.


class TimestampedModel(models.Model):
    """Model definition for TimestampedModel."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
