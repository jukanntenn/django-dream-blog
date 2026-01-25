from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager as DjangoCommentManager
from django_cte import CTEManager, CTEQuerySet
from markdown_field import MarkdownField

COMMENT_MAX_LENGTH = getattr(settings, "COMMENT_MAX_LENGTH", 3000)


class TreeCommentQuerySet(CTEQuerySet):
    def visible(self):
        return self.filter(is_public=True, is_removed=False)

    def roots(self):
        return self.visible().filter(parent__isnull=True)


class TreeCommentManager(DjangoCommentManager, CTEManager):
    pass


class TreeComment(CommentAbstractModel):
    comment = MarkdownField(_("comment"), max_length=COMMENT_MAX_LENGTH)
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

    def __str__(self):
        return "%s: %s..." % (self.name, self.comment.text[:50])

    @property
    def is_root(self):
        return self.parent is None

    @property
    def comment_html(self):
        return self.comment.html

    @property
    def anchor(self):
        return f"c{self.pk}"
