from core.utils import markdownify
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class EntryQuerySet(QuerySet):
    def published(self):
        return self.filter(
            publish_date__isnull=False,
            publish_date__lte=timezone.now(),
        )

    def visible(self):
        return self.published().filter(hidden=False)


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField(_("Created At"))
    modified_at = AutoLastModifiedField(_("Modified At"))

    class Meta:
        abstract = True


class RichContentModel(models.Model):
    content = models.TextField(_("Content"))

    @property
    def toc(self):
        return self.markdownified.get("toc", "")

    @property
    def content_html(self):
        return self.markdownified.get("content", "")

    @cached_property
    def markdownified(self):
        return markdownify(self.content)

    class Meta:
        abstract = True
