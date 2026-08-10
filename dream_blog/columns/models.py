from typing import cast

from django.conf import settings
from django.db import models
from django.db.models import Count, Manager, QuerySet
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from dream_blog.core.models import (
    AlertsModel,
    CommentsModel,
    EntryModelT,
    EntryQuerySet,
    HitCountModel,
    PreviousNextMixin,
    RichContentModel,
    TimeStampedModel,
)
from dream_blog.tags.models import TaggedItem


class ColumnQuerySet(EntryQuerySet[EntryModelT]):
    def visible(self) -> EntryQuerySet[EntryModelT]:
        return self.filter(hidden=False)

    def with_article_count(self) -> EntryQuerySet[EntryModelT]:
        return self.annotate(article_count=Count("article"))


class ColumnManager(Manager.from_queryset(ColumnQuerySet)):
    def visible(self) -> EntryQuerySet["Column"]:
        return cast("EntryQuerySet[Column]", self.get_queryset()).visible()

    def with_article_count(self) -> EntryQuerySet["Column"]:
        qs = cast("ColumnQuerySet[Column]", self.get_queryset())
        return qs.with_article_count()


class Column(HitCountModel, RichContentModel, TimeStampedModel, AlertsModel):
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True)
    excerpt = models.TextField(_("Excerpt"), blank=True)
    hidden = models.BooleanField(_("Hidden"), default=False)
    comments_enabled = models.BooleanField(_("Comments Enabled"), default=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
    )

    objects: ColumnManager = ColumnManager()
    article_set: QuerySet["Article"]
    article_count: int

    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")

    def __str__(self):
        return self.title

    @cached_property
    def num_articles(self):
        if hasattr(self, "article_count"):
            return self.article_count

        return self.article_set.count()

    def get_absolute_url(self):
        return reverse("columns:detail", kwargs={"slug": self.slug})


class ArticleQuerySet(EntryQuerySet[EntryModelT]):
    def visible(self) -> EntryQuerySet[EntryModelT]:
        return super().visible().filter(column__hidden=False)


class ArticleManager(Manager.from_queryset(ArticleQuerySet)):
    def visible(self) -> EntryQuerySet["Article"]:
        return cast("EntryQuerySet[Article]", self.get_queryset()).visible()


class Article(
    PreviousNextMixin,
    HitCountModel,
    RichContentModel,
    TimeStampedModel,
    CommentsModel,
    AlertsModel,
):
    title = models.CharField(_("Title"), max_length=200)
    publish_date = models.DateTimeField(
        _("Publish Date"),
        blank=True,
        null=True,
    )
    hidden = models.BooleanField(_("Hidden"), default=False)

    column = models.ForeignKey(
        Column,
        verbose_name=_("Column"),
        on_delete=models.CASCADE,
    )
    tags = TaggableManager(
        verbose_name=_("tags"),
        through=TaggedItem,
        blank=True,
    )

    objects: ArticleManager = ArticleManager()
    column_id: int

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

    @property
    def author(self):
        return self.column.author

    @property
    def prev(self):
        return self.get_next_or_previous(
            is_next=False,
            ordering=["publish_date"],
            column_id=self.column_id,
        )

    @property
    def next(self):
        return self.get_next_or_previous(
            is_next=True,
            ordering=["publish_date"],
            column_id=self.column_id,
        )

    def get_absolute_url(self):
        return reverse(
            "columns:article_detail",
            kwargs={"slug": self.column.slug, "pk": self.pk},
        )
