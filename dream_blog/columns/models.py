from core.models import (
    CommentsModel,
    EntryQuerySet,
    HitCountModel,
    RichContentModel,
    TimeStampedModel,
)
from django.conf import settings
from django.db import models
from django.db.models import Count, Manager, QuerySet
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class ColumnQuerySet(QuerySet):
    def visible(self):
        return self.filter(hidden=False)

    def with_article_count(self):
        return self.annotate(article_count=Count("article"))


class ColumnManager(Manager.from_queryset(ColumnQuerySet)):
    pass


class Column(HitCountModel, RichContentModel, TimeStampedModel):
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

    objects = ColumnManager()

    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")

    def __str__(self):
        return self.title

    @cached_property
    def num_articles(self):
        if hasattr(self, "article_count"):
            return getattr(self, "article_count")

        return self.article_set.count()

    def get_absolute_url(self):
        return reverse("columns:detail", kwargs={"slug": self.slug})


class ArticleQuerySet(EntryQuerySet):
    def visible(self):
        return super().visible().filter(column__hidden=False)


class ArticleManager(Manager.from_queryset(ArticleQuerySet)): ...


class Article(HitCountModel, RichContentModel, TimeStampedModel, CommentsModel):
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

    objects = ArticleManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

    @property
    def author(self):
        return self.column.author

    def get_absolute_url(self):
        return reverse(
            "columns:article_detail",
            kwargs={"slug": self.column.slug, "pk": self.pk},
        )
