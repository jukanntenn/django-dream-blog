from dataclasses import dataclass
from typing import Optional

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Value, CharField, IntegerField, Subquery, OuterRef
from django.db.models.functions import Cast
from django.urls import reverse

from hitcount.models import HitCount


@dataclass
class IndexEntry:
    """Wrapper for index page entry results from UNION query."""

    id: int
    title: str
    brief: str
    views: int
    parent_slug: Optional[str]
    parent_title: Optional[str]
    comment_count: int
    pub_date: str  # ISO format date string
    type: str  # 'p', 'a', or 'm'

    def get_absolute_url(self):
        """Get URL based on entry type."""
        if self.type == "p":
            return reverse("posts:detail", kwargs={"pk": self.id})
        elif self.type == "a":
            return reverse(
                "columns:article_detail",
                kwargs={"slug": self.parent_slug, "pk": self.id},
            )
        elif self.type == "m":
            return reverse(
                "tutorials:material_detail",
                kwargs={"slug": self.parent_slug, "pk": self.id},
            )


def _get_hit_count_subquery(model_class):
    """
    Returns a Subquery to fetch hit count for a given model.

    Uses Subquery because HitCount uses GenericRelation with object_pk as string.
    """
    ct = ContentType.objects.get_for_model(model_class)
    return Subquery(
        HitCount.objects.filter(
            object_pk=Cast(OuterRef("id"), CharField()),
            content_type=ct,
        ).values("hits")[:1],
        output_field=IntegerField(),
    )


def get_index_queryset():
    """
    Returns queryset combining Posts, Articles, and Materials.

    Uses Django's union() to combine different models at SQL level.
    Returns QuerySet with fields: id, title, brief, views, parent_slug,
    parent_title, comment_count, pub_date, type
    """
    # Use django.apps.get_model() to avoid inline imports
    Post = apps.get_model("posts", "Post")
    Article = apps.get_model("columns", "Article")
    Material = apps.get_model("tutorials", "Material")

    # Post queryset: type='p'
    posts_qs = (
        Post.objects.visible()
        .with_comment_count()
        .annotate(
            brief=F("excerpt"),
            views=_get_hit_count_subquery(Post),
            parent_slug=Value(None, output_field=CharField()),
            parent_title=Value(None, output_field=CharField()),
            pub_date=F("publish_date"),
            type=Value("p", output_field=CharField(max_length=1)),
        )
        .values(
            "id",
            "title",
            "brief",
            "views",
            "parent_slug",
            "parent_title",
            "comment_count",
            "pub_date",
            "type",
        )
    )

    # Article queryset: type='a'
    articles_qs = (
        Article.objects.visible()
        .with_comment_count()
        .select_related("column")
        .annotate(
            brief=Value("", output_field=CharField()),
            views=_get_hit_count_subquery(Article),
            parent_slug=F("column__slug"),
            parent_title=F("column__title"),
            pub_date=F("publish_date"),
            type=Value("a", output_field=CharField(max_length=1)),
        )
        .values(
            "id",
            "title",
            "brief",
            "views",
            "parent_slug",
            "parent_title",
            "comment_count",
            "pub_date",
            "type",
        )
    )

    # Material queryset: type='m'
    materials_qs = (
        Material.objects.visible()
        .with_comment_count()
        .select_related("tutorial")
        .annotate(
            brief=Value("", output_field=CharField()),
            views=_get_hit_count_subquery(Material),
            parent_slug=F("tutorial__slug"),
            parent_title=F("tutorial__title"),
            pub_date=F("publish_date"),
            type=Value("m", output_field=CharField(max_length=1)),
        )
        .values(
            "id",
            "title",
            "brief",
            "views",
            "parent_slug",
            "parent_title",
            "comment_count",
            "pub_date",
            "type",
        )
    )

    # Union and order by publish date DESC
    return posts_qs.union(articles_qs, materials_qs).order_by("-pub_date")
