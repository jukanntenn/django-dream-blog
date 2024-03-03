from core.utils import markdownify
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager as DjangoCommentManager
from django_cte import CTEManager, CTEQuerySet


class TreeCommentQuerySet(CTEQuerySet):
    def visible(self):
        return self.filter(is_public=True, is_removed=False)

    def roots(self):
        return self.visible().filter(parent__isnull=True)


class TreeCommentManager(DjangoCommentManager, CTEManager):
    pass


class TreeComment(CommentAbstractModel):
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    objects = TreeCommentManager.from_queryset(TreeCommentQuerySet)()

    class Meta(CommentAbstractModel.Meta):
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = None

    @property
    def is_root(self):
        return self.parent is None

    @property
    def comment_html(self):
        return markdownify(self.comment)["content"]

    @property
    def anchor(self):
        return f"c{self.pk}"
