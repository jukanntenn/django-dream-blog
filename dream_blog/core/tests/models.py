from core.models import (
    EntryQuerySet,
    PreviousNextMixin,
    RichContentModel,
    TimeStampedModel,
)
from django.db import models


class AbstractEntry(PreviousNextMixin, TimeStampedModel, RichContentModel):
    publish_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    hidden = models.BooleanField(default=False)

    objects = models.Manager.from_queryset(EntryQuerySet)()

    class Meta:
        abstract = True


class Entry(AbstractEntry):
    pass


class RankableEntry(AbstractEntry):
    rank = models.SmallIntegerField(unique=True)

    class Meta:
        ordering = ["rank"]
