from core.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class Alert(TimeStampedModel):
    text = models.TextField(_("Text"))
    show = models.BooleanField(_("Show"), default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    rank = models.IntegerField(_("Rank"), default=0)

    class Meta:
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")
        ordering = ["rank", "-created_at"]

    def __str__(self):
        return self.text[:30]
