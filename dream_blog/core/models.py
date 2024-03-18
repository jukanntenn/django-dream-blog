from core.utils import markdownify
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Count, Q, QuerySet
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCount, HitCountMixin
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from tree_comments.models import TreeComment


def _compensate(value):
    if value.startswith("--"):
        return value.lstrip("--")
    return value


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


class PreviousNextMixin:
    def get_next_or_previous(self, is_next, ordering=None, value_fields=None, **kwargs):
        if not self.pk:
            raise ValueError(
                _("get_next/get_previous cannot be used on unsaved objects.")
            )

        op = "gt" if is_next else "lt"
        order = "" if is_next else "-"

        if ordering is None:
            ordering = self._meta.ordering

        if not ordering:
            ordering = [self._meta.pk.name]

        param_field = ordering[0].lstrip("-")
        param_value = getattr(self, param_field)

        if ordering[0].startswith("-"):
            op = "lt" if is_next else "gt"

        q = Q(**{"%s__%s" % (param_field, op): param_value})

        if not self._meta.get_field(param_field).unique:
            op = "gt" if is_next else "lt"
            q = q | Q(**{param_field: param_value, "pk__%s" % op: self.pk})
            ordering.append("pk")

        qs = (
            self.__class__._default_manager.visible()
            .filter(**kwargs)
            .filter(q)
            .order_by(*[_compensate("%s%s" % (order, field)) for field in ordering])
        )

        if value_fields is not None:
            qs = qs.values(*value_fields)

        return qs.first()
