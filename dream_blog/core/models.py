from core.utils import markdownify
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Count, QuerySet
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCount, HitCountMixin
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from tree_comments.models import TreeComment


class EntryQuerySet(QuerySet):
    def published(self):
        return self.filter(
            publish_date__isnull=False,
            publish_date__lte=timezone.now(),
        )

    def visible(self):
        return self.published().filter(hidden=False)

    def with_comment_count(self):
        return self.annotate(comment_count=Count("comments"))


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


class CommentsModel(models.Model):
    comments_enabled = models.BooleanField(_("Comments Enabled"), default=True)
    comments = GenericRelation(
        TreeComment,
        content_type_field="content_type",
        object_id_field="object_pk",
    )

    class Meta:
        abstract = True

    @cached_property
    def num_comment_participants(self):
        return self.comments.values_list("user_id", flat=True).distinct().count()

    @cached_property
    def num_comments(self):
        if hasattr(self, "comment_count"):
            return getattr(self, "comment_count")

        return self.comments.visible().count()


class HitCountModel(HitCountMixin, models.Model):
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )

    class Meta:
        abstract = True

    @property
    def hits(self):
        return self.hit_count.hits
