from core.models import EntryQuerySet, RichContentModel, TimeStampedModel
from django.db import models


class Entry(TimeStampedModel, RichContentModel):
    publish_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    hidden = models.BooleanField(default=False)

    objects = models.Manager.from_queryset(EntryQuerySet)()
