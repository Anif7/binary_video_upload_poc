import uuid
from django.db import models
from model_utils.models import TimeStampedModel

class Status(models.IntegerChoices):
        INIT = 0, 'Initialized'
        UPLOADED = 1, 'Uploaded'
        FAILED = 2, 'Failed'
        

class VideoAsset(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    size = models.BigIntegerField(null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.INIT)

    def __str__(self):
        return f"{self.original_filename} ({self.get_status_display()})"
